from __future__ import annotations
import argparse, json, time, re, os
from typing import Dict, Any, Optional, Tuple, List

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers.generation.logits_process import LogitsProcessor, LogitsProcessorList

from .prompts import build_train_prompt, parse_answer

# ---------- misc utils ----------
def canonicalize_agent(name: Optional[str]) -> Optional[str]:
    if not name:
        return None
    s = re.sub(r"[^a-z0-9 ]+", "", name.strip().lower())
    if s in {"coder", "code", "developer", "dev", "programmer"}: return "coder"
    if s in {"analyst", "reasoner", "judge"}: return "analyst"
    if s in {"planner", "plan"}: return "planner"
    if s in {"web", "browser", "search", "web agent"}: return "web"
    if s in {"coordinator", "coord", "orchestrator"}: return "coordinator"
    return s or None

def line_count(path: str) -> int:
    n = 0
    with open(path, "r", encoding="utf-8") as f:
        for _ in f:
            n += 1
    return n

def pick_device(arg: str) -> str:
    arg = (arg or "auto").lower()
    if arg == "auto":
        if torch.backends.mps.is_available(): return "mps"
        if torch.cuda.is_available(): return "cuda"
        return "cpu"
    if arg in {"mps","cuda","cpu"}:
        if arg == "mps" and not torch.backends.mps.is_available(): return "cpu"
        if arg == "cuda" and not torch.cuda.is_available(): return "cpu"
        return arg
    return "cpu"

# ---------- optional chat wrapping (OFF by default) ----------
def wrap_with_chat_template(tok, user_text: str) -> str:
    if hasattr(tok, "apply_chat_template"):
        try:
            return tok.apply_chat_template(
                [{"role": "user", "content": user_text}],
                tokenize=False,
                add_generation_prompt=True,
            )
        except Exception:
            pass
    return user_text

# ---------- “paper-like” alt prompt (curiosity only) ----------
def to_paper_like_prompt(rec: Dict[str, Any]) -> str:
    sys = (
        "<|im_start|>system\n"
        "You are an attribution checker. Output a SINGLE LINE of strict JSON only.\n"
        'Schema: {\"who\": \"<AGENT_NAME_OR_UNKNOWN>\", \"when\": \"<STEP_OR_UNKNOWN>\"}\n'
        "Use EXACTLY the set {coder, analyst, planner, web, coordinator, unknown} for 'who'.\n"
        "Use a 0-based integer for 'when' if certain, else 'unknown'.\n"
        "<|im_end|>\n"
    )
    user = "<|im_start|>user\n{content}\n<|im_end|>\n<|im_start|>assistant\n".format(
        content=json.dumps(rec, ensure_ascii=False)
    )
    return sys + user

def to_prompt(rec: Dict[str, Any], use_trainfmt: bool, chat_wrap: bool, tok) -> str:
    if use_trainfmt:
        raw = build_train_prompt(rec.get("query",""), rec.get("steps", []) or [])
        return wrap_with_chat_template(tok, raw) if chat_wrap else raw
    base = to_paper_like_prompt(rec)
    return wrap_with_chat_template(tok, base) if chat_wrap else base

# ---------- sampling safety ----------
class NanInfLogitsProcessor(LogitsProcessor):
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor) -> torch.FloatTensor:
        scores = torch.nan_to_num(scores, nan=0.0, posinf=1e9, neginf=-1e9)
        return torch.clamp(scores, -1e9, 1e9)

def build_gen_kwargs(
    do_sample: bool,
    temperature: float,
    top_p: float,
    top_k: int,
    typical_p: Optional[float],
    pad_id: int,
    eos_id: int,
) -> Dict[str, Any]:
    kwargs: Dict[str, Any] = {
        "do_sample": do_sample,
        "num_beams": 1,
        "use_cache": True,
        "eos_token_id": eos_id,
        "pad_token_id": pad_id,
        "no_repeat_ngram_size": 3,
        "length_penalty": 1.0,
    }
    if not do_sample:
        kwargs["repetition_penalty"] = 1.02
        return kwargs
    t = max(1e-4, float(temperature))
    p = float(top_p) if 0.0 < float(top_p) <= 1.0 else 0.95
    k = int(top_k) if int(top_k) > 0 else 50
    kwargs.update({
        "temperature": t,
        "top_p": p,
        "top_k": k,
        "repetition_penalty": 1.0,
        "logits_processor": LogitsProcessorList([NanInfLogitsProcessor()]),
    })
    if typical_p is not None:
        tp = float(typical_p)
        kwargs["typical_p"] = tp if 0.0 < tp <= 1.0 else 0.9
    return kwargs

# ---------- robust decoding ----------
def safe_decode(tok, ids) -> str:
    try:
        return tok.decode(ids, skip_special_tokens=True)
    except Exception:
        if torch.is_tensor(ids): ids = ids.tolist()
        special = set(getattr(tok, "all_special_ids", []) or [])
        core_ids = [i for i in ids if i not in special]
        try:
            toks = tok.convert_ids_to_tokens(core_ids)
        except Exception:
            return ""
        toks = [(t if isinstance(t, str) else "") for t in toks]
        return "".join(toks)

# ---------- generation ----------
def _generate_continuation(
    model, tok, prompt: str, device: str,
    max_input_tokens: int, max_new_tokens: int,
    do_sample: bool, temperature: float, top_p: float, top_k: int, typical_p: Optional[float]
) -> str:
    model.eval()
    with torch.inference_mode():
        enc = tok(prompt, return_tensors="pt", truncation=True, max_length=max_input_tokens)
        enc = {k: v.to(device) for k, v in enc.items()}
        prompt_len = enc["input_ids"].shape[1]
        gen_kwargs = build_gen_kwargs(do_sample, temperature, top_p, top_k, typical_p, tok.pad_token_id, tok.eos_token_id)
        out = model.generate(**enc, max_new_tokens=max_new_tokens, **gen_kwargs)
        cont_ids = out[0, prompt_len:]
        return safe_decode(tok, cont_ids)

# ---------- inference w/ fallback ----------
def infer_with_fallback(
    model, tok, rec: Dict[str, Any], device: str,
    max_input_tokens: int, max_new_tokens: int,
    use_trainfmt: bool, chat_wrap: bool,
    do_sample: bool, temperature: float, top_p: float, top_k: int, typical_p: Optional[float]
):
    base_prompt = to_prompt(rec, use_trainfmt, chat_wrap, tok)

    # Pass 1
    text1 = _generate_continuation(
        model, tok, base_prompt, device, max_input_tokens, max_new_tokens,
        do_sample, temperature, top_p, top_k, typical_p
    )
    ans1 = parse_answer(text1) if use_trainfmt else None
    if ans1:
        return text1, ans1

    # Pass 2: answer-only nudge
    prompt2 = base_prompt + "\nNow return ONLY the <answer> line exactly as specified (no extra text)."
    text2 = _generate_continuation(
        model, tok, prompt2, device, max_input_tokens, 16,
        do_sample, temperature, top_p, top_k, typical_p
    )
    ans2 = parse_answer(text2) if use_trainfmt else None
    if ans2:
        return text2, ans2

    return text1, None

# ---------- main ----------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, help="HF repo id or local folder path for the policy.")
    ap.add_argument("--tokenizer", default=None, help="Tokenizer source (HF id). If omitted, use --model.")
    ap.add_argument("--data", required=True)
    ap.add_argument("--device", type=str, default="auto")
    ap.add_argument("--trainfmt", action="store_true", help="use training-format prompt/parse")
    ap.add_argument("--paper-like", action="store_true", help="use JSON-style prompt (curiosity only)")
    ap.add_argument("--chat-wrap", action="store_true", help="wrap prompt with tokenizer chat template (OFF by default)")
    ap.add_argument("--max-input-tokens", type=int, default=384)
    ap.add_argument("--max-new-tokens", type=int, default=64)

    # sampling knobs
    ap.add_argument("--do-sample", action="store_true")
    ap.add_argument("--temperature", type=float, default=0.7)
    ap.add_argument("--top_p", type=float, default=0.8)
    ap.add_argument("--top_k", type=int, default=20)
    ap.add_argument("--typical-p", type=float, default=None)

    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--progress-every", type=int, default=5)
    ap.add_argument("--save-preds", type=str, default=None)
    args = ap.parse_args()

    if args.trainfmt and args.paper_like:
        raise SystemExit("Choose one: --trainfmt OR --paper-like")

    device = pick_device(args.device)
    print(f"-> Using device: {device}")
    print(f"[eval] tokenizer source: {args.tokenizer or args.model}")

    tok_src = args.tokenizer or args.model
    tok = AutoTokenizer.from_pretrained(tok_src, use_fast=False, trust_remote_code=True)
    if tok.pad_token_id is None:
        tok.pad_token = tok.eos_token

    # Handle local folder hints early (better error than HFValidationError)
    if os.path.sep in args.model or args.model.startswith("."):
        if not os.path.isdir(args.model):
            print(f"Local model folder not found: {args.model}\nDid training finish and save to 'epoch00-final'? Check the path.", flush=True)
            raise SystemExit(1)

    dtype = torch.float16 if device in ("mps", "cuda") else torch.float32
    model = AutoModelForCausalLM.from_pretrained(
        args.model, torch_dtype=dtype, low_cpu_mem_usage=False, trust_remote_code=True
    ).to(device)
    model.eval()
    model.config.use_cache = True

    total = line_count(args.data)
    if args.limit:
        total = min(total, args.limit)

    n = agent_ok = step_ok = both_ok = 0
    t0 = time.time()
    pred_f = open(args.save_preds, "w", encoding="utf-8") if args.save_preds else None

    with open(args.data, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            rec = json.loads(line)

            text, parsed = infer_with_fallback(
                model, tok, rec, device,
                max_input_tokens=args.max_input_tokens,
                max_new_tokens=args.max_new_tokens,
                use_trainfmt=args.trainfmt,
                chat_wrap=args.chat_wrap,
                do_sample=args.do_sample,
                temperature=args.temperature,
                top_p=args.top_p,
                top_k=args.top_k,
                typical_p=args.typical_p,
            )

            who_pred = None
            step_pred = None
            if parsed:
                who_pred, step_pred = parsed
                who_pred = canonicalize_agent(who_pred)

            lab = rec.get("label") or {}
            agent_gt = canonicalize_agent(lab.get("agent"))
            step_gt = lab.get("step")

            a_ok = (agent_gt is not None and who_pred is not None and agent_gt == who_pred)
            s_ok = (isinstance(step_gt, int) and isinstance(step_pred, int) and step_gt == step_pred)
            agent_ok += int(a_ok)
            step_ok  += int(s_ok)
            both_ok  += int(a_ok and s_ok)
            n += 1

            if pred_f:
                plain_head = (build_train_prompt(rec.get("query",""), rec.get("steps", []) or [])[:180]
                              if args.trainfmt else to_paper_like_prompt(rec)[:180])
                pred_f.write(json.dumps({
                    "i": i,
                    "id": rec.get("id"),
                    "who_pred": who_pred,
                    "step_pred_idx0": step_pred,
                    "label_agent": agent_gt,
                    "label_step_idx0": step_gt,
                    "raw": (text or "").strip(),
                    "prompt_head": plain_head,
                }, ensure_ascii=False) + "\n")

            if i % max(1, args.progress_every) == 0:
                dt = time.time() - t0
                ips = i / max(dt, 1e-6)
                eta = (total - i) / max(ips, 1e-6)
                print(f"...processed {i}/{total} items | elapsed={dt:.1f}s | items/sec={ips:.3f} | ETA~{eta:.1f}s", flush=True)

            if args.limit and n >= args.limit:
                break

    if pred_f:
        pred_f.close()

    print({
        "samples": n,
        "agent_acc": round(agent_ok / max(1, n), 3),
        "step_acc":  round(step_ok  / max(1, n), 3),
        "both_acc":  round(both_ok  / max(1, n), 3),
    })

if __name__ == "__main__":
    main()

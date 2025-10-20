from __future__ import annotations
import argparse, json, time, re
from typing import Dict, Any, Optional, Tuple

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, StoppingCriteria, StoppingCriteriaList

from .prompts import build_train_prompt, parse_answer

# ----------------- device -----------------
def pick_device(arg: str) -> str:
    arg = (arg or "auto").lower()
    if arg == "auto":
        return "mps" if torch.backends.mps.is_available() else "cpu"
    if arg in {"mps", "cpu"}:
        return arg if (arg != "mps" or torch.backends.mps.is_available()) else "cpu"
    return "cpu"

# ----------------- small utils -----------------
def line_count(path: str) -> int:
    n = 0
    with open(path, "r", encoding="utf-8") as f:
        for _ in f:
            n += 1
    return n

def canonicalize_agent(name: Optional[str]) -> Optional[str]:
    if not name:
        return None
    s = re.sub(r"[^a-z0-9 ]+", "", name.strip().lower())
    if s in {"coder","code","developer","dev","programmer"}: return "coder"
    if s in {"analyst","reasoner","judge"}: return "analyst"
    if s in {"planner","plan"}: return "planner"
    if s in {"web","browser","search","web agent"}: return "web"
    if s in {"coordinator","coord","orchestrator"}: return "coordinator"
    return s or None

def to_prompt(rec: Dict[str, Any]) -> str:
    q = rec.get("query", "") or ""
    steps = rec.get("steps", []) or []
    return build_train_prompt(q, steps)

# ----------------- heuristic fallback (optional) -----------------
_ERROR_WORDS = [
    "error","exception","traceback","keyerror","typeerror","valueerror",
    "indexerror","zerodivisionerror","filenotfounderror","runtimeerror",
    "assertionerror","nameerror","attributerror","timeout","failed","crash"
]

def _looks_like_error(obj: Any) -> bool:
    if isinstance(obj, dict):
        err = obj.get("error", None)
        if err and str(err).strip().lower() not in {"", "none", "null"}:
            return True
        low = " ".join(str(v) for v in obj.values()).lower()
    else:
        low = str(obj).lower()
    return any(w in low for w in _ERROR_WORDS)

def heuristic_who_when(rec: Dict[str, Any]) -> Tuple[Optional[str], Optional[int]]:
    steps = rec.get("steps") or []
    for i, s in enumerate(steps):
        if _looks_like_error(s):
            agent = None
            if isinstance(s, dict) and "agent" in s:
                agent = canonicalize_agent(str(s.get("agent", "")))
            return agent, i
    return None, None

# ----------------- generation -----------------
class StopOnAnswer(StoppingCriteria):
    def __init__(self, tok: AutoTokenizer, lookback: int = 512):
        super().__init__()
        self.tok = tok
        self.lookback = lookback
        self.stop = "</answer>"
    def __call__(self, input_ids, scores, **kw):
        text = self.tok.decode(input_ids[0][-self.lookback:], skip_special_tokens=True)
        return self.stop in text

def _generate_continuation(
    model, tok, prompt: str, device: str,
    max_input_tokens: int, max_new_tokens: int, stop: bool
) -> str:
    model.eval()
    with torch.inference_mode():
        enc = tok(prompt, return_tensors="pt", truncation=True, max_length=max_input_tokens)
        enc = {k: v.to(device) for k, v in enc.items()}
        prompt_len = enc["input_ids"].shape[1]
        kwargs = dict(
            max_new_tokens=max_new_tokens,
            do_sample=False,
            num_beams=1,
            use_cache=True,
            pad_token_id=tok.pad_token_id,
            eos_token_id=tok.eos_token_id,
            repetition_penalty=1.02,
        )
        if stop:
            kwargs["stopping_criteria"] = StoppingCriteriaList([StopOnAnswer(tok)])
        out = model.generate(**enc, **kwargs)
        cont = out[0, prompt_len:]
        return tok.decode(cont, skip_special_tokens=True)

def infer_with_fallback(
    model, tok, rec: Dict[str, Any], device: str,
    max_input_tokens: int, max_new_tokens: int
):
    base_prompt = to_prompt(rec)

    # Pass 1
    text1 = _generate_continuation(model, tok, base_prompt, device, max_input_tokens, max_new_tokens, stop=True)
    ans1 = parse_answer(text1)
    if ans1:
        return text1, ans1

    # Pass 2
    prompt2 = base_prompt + "\nNow return ONLY the <answer> line exactly as specified (no extra text)."
    text2 = _generate_continuation(model, tok, prompt2, device, max_input_tokens, 32, stop=True)
    ans2 = parse_answer(text2)
    if ans2:
        return text2, ans2

    # Pass 3: heuristic
    who_h, step_h = heuristic_who_when(rec)
    if (who_h is not None) or (step_h is not None):
        return text1, (who_h or None, step_h)

    return text1, None

# ----------------- main -----------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--max-new-tokens", type=int, default=24)
    ap.add_argument("--max-input-tokens", type=int, default=384)
    ap.add_argument("--device", type=str, default="auto")  # auto|mps|cpu
    ap.add_argument("--progress-every", type=int, default=5)
    ap.add_argument("--save-preds", type=str, default=None)
    args = ap.parse_args()

    device = pick_device(args.device)
    print(f"-> Using device: {device}")

    tok = AutoTokenizer.from_pretrained(args.model, use_fast=False, trust_remote_code=True)
    if tok.pad_token_id is None:
        tok.pad_token = tok.eos_token

    dtype = torch.float16 if device == "mps" else torch.float32
    model = AutoModelForCausalLM.from_pretrained(
        args.model, torch_dtype=dtype, low_cpu_mem_usage=False, trust_remote_code=True
    ).to(device)
    model.eval()
    model.config.use_cache = True

    total = line_count(args.data)
    if args.limit:
        total = min(total, args.limit)

    pred_f = open(args.save_preds, "w", encoding="utf-8") if args.save_preds else None

    n = agent_ok = step_ok = both_ok = 0
    t0 = time.time()

    with open(args.data, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            rec = json.loads(line)

            text, parsed = infer_with_fallback(
                model, tok, rec, device,
                max_input_tokens=args.max_input_tokens,
                max_new_tokens=args.max_new_tokens,
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

            if pred_f:
                pred_f.write(json.dumps({
                    "i": i,
                    "id": rec.get("id"),
                    "who_pred": who_pred,
                    "step_pred_idx0": step_pred,
                    "label_agent": agent_gt,
                    "label_step_idx0": step_gt,
                    "raw": (text or "").strip(),
                    "prompt_head": (to_prompt(rec)[:180] if isinstance(rec, dict) else ""),
                }, ensure_ascii=False) + "\n")

            n += 1
            if i % max(1, args.progress_every) == 0:
                dt = time.time() - t0
                ips = i / max(dt, 1e-6)
                eta = (total - i) / max(ips, 1e-6)
                print(f"...processed {i}/{total} | {ips:.2f} it/s | ETA~{eta:.1f}s", flush=True)

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

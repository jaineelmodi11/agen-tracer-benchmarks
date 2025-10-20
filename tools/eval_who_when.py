from __future__ import annotations
import argparse, json, os, re, sys, math, random
from typing import List, Dict, Any, Optional, Tuple

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

ALLOWED_WHO = {"tool", "model", "env"}
ALLOWED_WHEN = {"plan", "toolcall", "reflect", "final"}

SYS_PROMPT = (
    "You are a precise evaluator for agent failures. "
    "Answer ONLY with a strict JSON object like: "
    '{"who":"model","when":"plan"}. '
    "Valid who: tool, model, env. "
    "Valid when: plan, toolcall, reflect, final."
)

USER_TEMPLATE = """Question:
{question}

Task: Identify WHO caused the failure and WHEN it was induced.

Return ONLY JSON with exactly two keys:
{{
  "who": "<tool|model|env>",
  "when": "<plan|toolcall|reflect|final>"
}}"""

def set_seed(seed: int):
    random.seed(seed)
    torch.manual_seed(seed)

def _normalize_who(x: str) -> str:
    x = (x or "").strip().lower()
    if x in ALLOWED_WHO: return x
    # loose synonyms
    if x in {"environment", "runtime", "executor"}: return "env"
    if x in {"llm", "agent", "planner", "policy"}: return "model"
    if x in {"function", "api", "tooling", "tools"}: return "tool"
    return "model"  # safe default

def _normalize_when(x: str) -> str:
    x = (x or "").strip().lower()
    if x in ALLOWED_WHEN: return x
    if x in {"planning"}: return "plan"
    if x in {"tool_call", "tool-call", "call", "act"}: return "toolcall"
    if x in {"reflection", "reflecting"}: return "reflect"
    if x in {"final_answer", "answer", "output"}: return "final"
    return "final"  # safe default

def extract_json_block(text: str) -> Optional[Dict[str, Any]]:
    # Try strict first
    try:
        obj = json.loads(text.strip())
        if isinstance(obj, dict): return obj
    except Exception:
        pass
    # Fallback: grab first {...} block
    m = re.search(r"\{.*?\}", text, flags=re.S)
    if m:
        s = m.group(0)
        try:
            obj = json.loads(s)
            if isinstance(obj, dict): return obj
        except Exception:
            pass
    # Fallback: bare label lines
    who = None
    when = None
    mw = re.search(r'who\s*[:=]\s*"?([A-Za-z_ -]+)"?', text, flags=re.I)
    if mw: who = mw.group(1)
    mn = re.search(r'when\s*[:=]\s*"?([A-Za-z_ -]+)"?', text, flags=re.I)
    if mn: when = mn.group(1)
    if who or when:
        return {"who": who, "when": when}
    return None

def build_prompt(tok, use_chat_template: bool, question: str) -> str | Dict[str, Any]:
    if use_chat_template and hasattr(tok, "apply_chat_template"):
        msgs = [
            {"role": "system", "content": SYS_PROMPT},
            {"role": "user", "content": USER_TEMPLATE.format(question=question)},
        ]
        return tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
    # fallback plain prompt
    return SYS_PROMPT + "\n\n" + USER_TEMPLATE.format(question=question) + "\n"

def batched(iterable, n):
    buf = []
    for x in iterable:
        buf.append(x)
        if len(buf) == n:
            yield buf
            buf = []
    if buf: yield buf

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--tokenizer", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--device", default="")
    ap.add_argument("--batch", type=int, default=4)
    ap.add_argument("--max-new", type=int, default=128)
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--top-p", type=float, default=1.0)
    ap.add_argument("--use-chat-template", action="store_true")
    ap.add_argument("--seed", type=int, default=1234)
    args = ap.parse_args()

    set_seed(args.seed)

    device = args.device or ("mps" if torch.backends.mps.is_available()
                             else "cuda" if torch.cuda.is_available() else "cpu")

    # load data
    rows = []
    with open(args.data, "r", encoding="utf-8") as f:
        for ln in f:
            if ln.strip():
                rows.append(json.loads(ln))
    print(f"Loaded {len(rows)} items from {args.data}")

    tok = AutoTokenizer.from_pretrained(args.tokenizer, trust_remote_code=True)
    if getattr(tok, "pad_token_id", None) is None:
        if getattr(tok, "eos_token_id", None) is not None:
            tok.pad_token_id = tok.eos_token_id
            if getattr(tok, "eos_token", None) is not None:
                tok.pad_token = tok.eos_token
    tok.truncation_side = "left"
    tok.padding_side = "left"

    model = AutoModelForCausalLM.from_pretrained(args.model, trust_remote_code=True)
    model = model.to(device)
    model.eval()
    try:
        model.config.use_cache = True
    except Exception:
        pass

    do_sample = args.temperature and args.temperature > 0
    eos_ids = []
    for tok_str in ["<|im_end|>", "<|eot_id|>"]:
        try:
            tid = tok.convert_tokens_to_ids(tok_str)
            if isinstance(tid, int) and tid != tok.unk_token_id and tid not in (-1, None):
                eos_ids.append(tid)
        except Exception:
            pass
    if tok.eos_token_id is not None:
        if isinstance(tok.eos_token_id, int):
            eos_ids.append(tok.eos_token_id)
        else:
            eos_ids.extend([x for x in tok.eos_token_id if isinstance(x, int)])
    eos_ids = list(dict.fromkeys([x for x in eos_ids if x is not None]))

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    fout = open(args.out, "w", encoding="utf-8")

    total = len(rows)
    done = 0
    for chunk in batched(rows, max(1, args.batch)):
        prompts = [
            build_prompt(tok, args.use_chat_template, r.get("question", r.get("input", "")))
            for r in chunk
        ]
        enc = tok(prompts, return_tensors="pt", padding=True, truncation=True)
        enc = {k: v.to(device) for k, v in enc.items()}

        gen_kwargs = dict(
            max_new_tokens=args.max_new,
            do_sample=bool(do_sample),
            top_p=float(args.top_p) if do_sample else None,
            temperature=float(args.temperature) if do_sample else None,
            pad_token_id=tok.pad_token_id,
            eos_token_id=eos_ids if len(eos_ids) > 1 else (eos_ids[0] if eos_ids else None),
            return_dict_in_generate=True,
        )

        with torch.inference_mode():
            out = model.generate(**enc, **{k: v for k, v in gen_kwargs.items() if v is not None})

        seqs = getattr(out, "sequences", out)
        if seqs.ndim == 1:
            seqs = seqs.unsqueeze(0)
        cont = seqs[:, enc["input_ids"].shape[1]:]
        texts = tok.batch_decode(cont, skip_special_tokens=True)

        for row, txt in zip(chunk, texts):
            parsed = extract_json_block(txt) or {}
            who = _normalize_who(parsed.get("who", "model"))
            when = _normalize_when(parsed.get("when", "final"))
            rec = {
                "id": row.get("id") or row.get("instance_id") or row.get("qid"),
                "question": row.get("question", ""),
                "who_pred": who,
                "when_pred": when,
                "raw": txt.strip(),
                "model_name_or_path": args.model,
            }
            fout.write(json.dumps(rec) + "\n")
            done += 1

        print(f"[batch] {done}/{total} done", flush=True)

    fout.close()
    print(f"Wrote predictions to {args.out}")

if __name__ == "__main__":
    main()

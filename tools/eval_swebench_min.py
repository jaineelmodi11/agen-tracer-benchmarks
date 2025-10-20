from __future__ import annotations
import argparse, json, os, sys, re, time
from typing import List, Dict, Any

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# --- quiet noisy libs early
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")

def _maybe_apply_chat_template(tok, user_content: str, use_chat: bool) -> str:
    if not use_chat or not hasattr(tok, "apply_chat_template"):
        return user_content
    msgs = [
        {"role": "system", "content":
         "You are a senior software engineer. Produce a **minimal, self-contained** fix.\n"
         "If a gold answer is expected, output it plainly. If a code patch is expected, return only the patch text."},
        {"role": "user", "content": user_content},
    ]
    return tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)

def _end_ids_for_qwen(tok) -> List[int]:
    ids: List[int] = []
    for t in ["<|im_end|>", "<|eot_id|>"]:
        try:
            tid = tok.convert_tokens_to_ids(t)
            if isinstance(tid, int) and tid != tok.unk_token_id and tid not in (-1, None):
                ids.append(tid)
        except Exception:
            pass
    if tok.eos_token_id is not None:
        if isinstance(tok.eos_token_id, int):
            ids.append(tok.eos_token_id)
        else:
            ids.extend([x for x in tok.eos_token_id if isinstance(x, int)])
    # dedup
    ids = [x for i, x in enumerate(ids) if x is not None and x not in ids[:i]]
    return ids or ([tok.eos_token_id] if tok.eos_token_id is not None else [])

def _build_prompt(item: Dict[str, Any]) -> str:
    """
    Accepts flexible 'lite' JSONL formats.
    Priority:
      1) item['prompt']
      2) compose from fields like: repo, issue, failing_tests, context, gold (optional)
    """
    if "prompt" in item and item["prompt"]:
        return item["prompt"]

    repo = item.get("repo", "<unknown-repo>")
    title = item.get("title", "")
    issue = item.get("issue", item.get("description", ""))
    failing = item.get("failing_tests", [])
    ctx = item.get("context", "")
    goal_hint = ""
    if "gold" in item:
        goal_hint = "\n(There is a single gold answer expected; output it exactly if you know it.)"

    parts = [
        f"Repository: {repo}",
        f"Title: {title}" if title else "",
        "Issue:\n" + issue if issue else "",
        ("Failing tests:\n- " + "\n- ".join(failing)) if failing else "",
        ("Context:\n" + ctx) if ctx else "",
        goal_hint,
        "",
        "Produce the minimal fix or final answer. Output only your final result (no explanations)."
    ]
    return "\n".join([p for p in parts if p])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--tokenizer", required=True)
    ap.add_argument("--dataset", required=True, help="JSONL file (lite format)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-new", type=int, default=256)
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--top-p", type=float, default=1.0)
    ap.add_argument("--device", default="")
    ap.add_argument("--batch", type=int, default=1)
    ap.add_argument("--timeout-s", type=int, default=900)  # kept for API parity; not used directly
    ap.add_argument("--use-chat-template", action="store_true")
    args = ap.parse_args()

    # Load data
    items: List[Dict[str, Any]] = []
    with open(args.dataset, "r", encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if not ln:
                continue
            items.append(json.loads(ln))
    print(f"Loaded {len(items)} items from {args.dataset}")

    # Model / tok
    device = args.device or ("mps" if torch.backends.mps.is_available()
                             else "cuda" if torch.cuda.is_available() else "cpu")
    tok = AutoTokenizer.from_pretrained(args.tokenizer, trust_remote_code=True)
    if getattr(tok, "pad_token_id", None) is None and getattr(tok, "eos_token_id", None) is not None:
        tok.pad_token_id = tok.eos_token_id
        if getattr(tok, "eos_token", None) is not None:
            tok.pad_token = tok.eos_token
    tok.truncation_side = "left"
    tok.padding_side = "left"

    model = AutoModelForCausalLM.from_pretrained(args.model, trust_remote_code=True)
    model = model.to(device)
    model.eval()
    try:
        model.config.use_cache = False
    except Exception:
        pass
    try:
        if hasattr(model, "generation_config"):
            gc = model.generation_config
            if getattr(gc, "pad_token_id", None) is None and tok.pad_token_id is not None:
                gc.pad_token_id = tok.pad_token_id
            if getattr(gc, "eos_token_id", None) is None and tok.eos_token_id is not None:
                gc.eos_token_id = tok.eos_token_id
    except Exception:
        pass

    # Gen settings
    do_sample = args.temperature and args.temperature > 0
    eos_ids = _end_ids_for_qwen(tok)
    gen_common = dict(
        do_sample=bool(do_sample),
        max_new_tokens=int(args.max_new),
        pad_token_id=tok.pad_token_id,
        eos_token_id=eos_ids if len(eos_ids) > 1 else eos_ids[0] if eos_ids else None,
        use_cache=True,
        return_dict_in_generate=True,
    )
    if do_sample:
        gen_common["temperature"] = float(args.temperature)
        gen_common["top_p"] = float(args.top_p)

    # Stream write
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    out_f = open(args.out, "w", encoding="utf-8")
    total = len(items)
    bsz = max(1, int(args.batch))

    t0 = time.time()
    for start in range(0, total, bsz):
        batch = items[start:start+bsz]
        ids = []
        prompts = []
        for it in batch:
            iid = it.get("instance_id") or it.get("id") or it.get("slug") or f"ex-{start}"
            ids.append(str(iid))
            user_prompt = _build_prompt(it)
            prompts.append(_maybe_apply_chat_template(tok, user_prompt, args.use_chat_template))

        enc = tok(prompts, return_tensors="pt", padding=True, truncation=True)
        enc = {k: v.to(device) for k, v in enc.items()}
        with torch.inference_mode():
            out = model.generate(**enc, **gen_common)

        seq = getattr(out, "sequences", out)
        if isinstance(seq, torch.Tensor) and seq.ndim == 1:
            seq = seq.unsqueeze(0)

        inp_len = enc["input_ids"].shape[1]
        cont = seq[:, inp_len:]
        texts = tok.batch_decode(cont, skip_special_tokens=True)

        for iid, txt in zip(ids, texts):
            obj = {
                "instance_id": iid,
                "completion": txt.strip()
            }
            out_f.write(json.dumps(obj) + "\n")
        out_f.flush()
        done = min(total, start+bsz)
        eta = (time.time()-t0) / max(1, done) * (total-done)
        print(f"[batch] {done}/{total} done  (ETA ~{int(eta)}s)", flush=True)

    out_f.close()
    print(f"Wrote predictions to {args.out}")

if __name__ == "__main__":
    main()

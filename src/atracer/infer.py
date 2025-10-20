# src/atracer/infer.py
import argparse
import json
import sys
from typing import Optional

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    StoppingCriteria,
    StoppingCriteriaList,
    LogitsProcessor,
    LogitsProcessorList,
)

def pick_device(arg: str) -> str:
    arg = (arg or "auto").lower()
    if arg == "auto":
        return "mps" if torch.backends.mps.is_available() else "cpu"
    if arg in {"mps", "cpu"}:
        if arg == "mps" and not torch.backends.mps.is_available():
            print("⚠️  MPS requested but not available; falling back to CPU.", file=sys.stderr)
            return "cpu"
        return arg
    return "cpu"

class StopOnJSONClose(StoppingCriteria):
    def __init__(self, tokenizer, start_from: int):
        super().__init__()
        self.tokenizer = tokenizer
        self.start_from = start_from
    def __call__(self, input_ids, scores, **kwargs) -> bool:
        gen_ids = input_ids[0][self.start_from:]
        if gen_ids.numel() == 0:
            return False
        tail = self.tokenizer.decode(gen_ids[-96:], skip_special_tokens=True)
        return "{" in tail and "}" in tail

class BlockEOSTillJSONClose(LogitsProcessor):
    def __init__(self, tokenizer, start_from: int, eos_token_id: Optional[int]):
        self.tokenizer = tokenizer
        self.start_from = start_from
        self.eos = eos_token_id
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor) -> torch.FloatTensor:
        if self.eos is None:
            return scores
        gen_ids = input_ids[0][self.start_from:]
        if gen_ids.numel() == 0:
            return scores
        tail = self.tokenizer.decode(gen_ids[-128:], skip_special_tokens=True)
        if "{" in tail and "}" not in tail:
            scores[:, self.eos] = float("-inf")
        return scores

def generate_json(
    model,
    tok,
    prompt: str,
    *,
    device: str = "cpu",
    max_input_tokens: int = 384,
    max_new_tokens: int = 32,
    temperature: float = 0.2,
    top_p: float = 0.95,
):
    model.eval()
    with torch.inference_mode():
        enc = tok(prompt, return_tensors="pt", truncation=True, max_length=max_input_tokens)
        enc = {k: v.to(device) for k, v in enc.items()}
        prompt_len = enc["input_ids"].shape[1]

        stops = StoppingCriteriaList([StopOnJSONClose(tok, start_from=prompt_len)])
        lp = LogitsProcessorList([BlockEOSTillJSONClose(tok, start_from=prompt_len, eos_token_id=tok.eos_token_id)])

        out = model.generate(
            **enc,
            max_new_tokens=max_new_tokens,
            min_new_tokens=8,
            do_sample=(temperature > 0.0),
            temperature=max(1e-6, temperature),
            top_p=top_p,
            num_beams=1,
            use_cache=True,
            pad_token_id=tok.pad_token_id,
            eos_token_id=None,
            logits_processor=lp,
            stopping_criteria=stops,
            repetition_penalty=1.05,
        )
        cont = out[0, prompt_len:]
        return tok.decode(cont, skip_special_tokens=True)

def main():
    from .schema import Record
    from .prompts import build_prompt
    from .parsing import extract_answer

    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--jsonl", required=True)
    ap.add_argument("--device", default="auto", help="auto|mps|cpu")
    ap.add_argument("--max-input-tokens", type=int, default=384)
    ap.add_argument("--max-new-tokens", type=int, default=32)
    ap.add_argument("--temperature", type=float, default=0.2)
    ap.add_argument("--top_p", type=float, default=0.95)
    args = ap.parse_args()

    device = pick_device(args.device)
    torch.set_num_threads(4)
    torch.set_num_interop_threads(1)

    tok = AutoTokenizer.from_pretrained(args.model, use_fast=True)
    if tok.pad_token_id is None:
        tok.pad_token = tok.eos_token

    dtype = torch.float16 if device == "mps" else torch.float32
    model = AutoModelForCausalLM.from_pretrained(
        args.model, torch_dtype=dtype, low_cpu_mem_usage=False
    ).to(device)

    with open(args.jsonl, "r", encoding="utf-8") as f:
        for line in f:
            rec = Record(**json.loads(line))
            prompt = build_prompt(rec)
            text = generate_json(
                model, tok, prompt,
                device=device,
                max_input_tokens=args.max_input_tokens,
                max_new_tokens=args.max_new_tokens,
                temperature=args.temperature,
                top_p=args.top_p,
            )
            ans = extract_answer(text) or (None, None)
            print(rec.id, "->", ans, "\nRAW:\n", text)

if __name__ == "__main__":
    main()

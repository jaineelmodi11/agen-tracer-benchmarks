# src/atracer/reasoner.py
from transformers import AutoTokenizer, AutoModelForCausalLM

class AttributionReasoner:
    def __init__(self, path_or_hub):
        self.tok = AutoTokenizer.from_pretrained(path_or_hub, use_fast=False, trust_remote_code=True)
        self.m = AutoModelForCausalLM.from_pretrained(path_or_hub, trust_remote_code=True)
        if self.tok.pad_token is None: self.tok.pad_token = self.tok.eos_token

    def predict(self, query, steps, max_new_tokens=32):
        from .prompts import build_train_prompt
        from .parsing import parse_answer
        prompt = build_train_prompt(query, steps)
        enc = self.tok(prompt, return_tensors="pt")
        out = self.m.generate(**enc, max_new_tokens=max_new_tokens, do_sample=False)
        text = self.tok.decode(out[0][enc["input_ids"].shape[1]:], skip_special_tokens=True)
        who, when = parse_answer(text)
        return {"who": who, "when": when, "raw": text}

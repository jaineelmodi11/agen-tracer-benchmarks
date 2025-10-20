# smoke_test.py
from transformers import AutoTokenizer, AutoModelForCausalLM, StoppingCriteria, StoppingCriteriaList
import json, torch
from src.atracer.prompts import build_train_prompt

ckpt = "checkpoints/atracer-qwenrl-0p5b/epoch15-upd064"  # pick any saved dir

tok = AutoTokenizer.from_pretrained(ckpt, use_fast=False, trust_remote_code=True)
mdl = AutoModelForCausalLM.from_pretrained(ckpt, trust_remote_code=True, torch_dtype=torch.float16).to("mps")
if tok.pad_token_id is None: tok.pad_token = tok.eos_token

ex = json.loads(open("data/who_when.test.withG.jsonl").readline())
prompt = build_train_prompt(ex["query"], ex["steps"])

class StopOnAnswer(StoppingCriteria):
    def __init__(self, t): self.t=t; self.stop="</answer>"
    def __call__(self, input_ids, scores, **kw):
        return self.stop in self.t.decode(input_ids[0][-160:], skip_special_tokens=True)

ids = tok(prompt, return_tensors="pt", truncation=True, max_length=384).to("mps")
out = mdl.generate(
    **ids,
    max_new_tokens=64,
    do_sample=False, temperature=0.0, top_p=1.0,
    use_cache=True, num_beams=1,
    stopping_criteria=StoppingCriteriaList([StopOnAnswer(tok)]),
    pad_token_id=tok.eos_token_id, eos_token_id=tok.eos_token_id,
)
print(tok.decode(out[0], skip_special_tokens=True))

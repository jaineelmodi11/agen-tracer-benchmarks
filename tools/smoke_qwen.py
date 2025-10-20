from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

ckpt = "checkpoints/atracer-ppo-qwen0p5b-fixed/epoch00-final"

device = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")

tok = AutoTokenizer.from_pretrained(ckpt, trust_remote_code=True)
tok.truncation_side = "left"
tok.padding_side    = "left"
if tok.pad_token_id is None:
    tok.pad_token = tok.eos_token

m = AutoModelForCausalLM.from_pretrained(ckpt, trust_remote_code=True).eval().to(device)

msgs = [{"role":"user","content":"Say 'hello world' then END. At the VERY END, output ONLY: coder 3"}]

# Use chat template if present, but build the attention mask yourself
prompt_str = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
enc = tok(prompt_str, return_tensors="pt", padding=True, truncation=True, max_length=384)
enc = {k:v.to(device) for k,v in enc.items()}

out = m.generate(**enc, max_new_tokens=24, do_sample=False,
                 eos_token_id=tok.eos_token_id, pad_token_id=tok.pad_token_id)
print(tok.decode(out[0][enc["input_ids"].shape[1]:], skip_special_tokens=True))

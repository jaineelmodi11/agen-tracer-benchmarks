#!/usr/bin/env python3
import argparse, json, sys, torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def pick_prompt(row):
    # choose a prompt field; supports both your “remap + tail” files and raw eval
    for k in ("query","prompt","input"):
        if k in row and row[k]:
            return row[k]
    # messages-style (trainfmt) fallback
    if "messages" in row and isinstance(row["messages"], list):
        return row["messages"]  # we'll apply chat template
    return ""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--tokenizer", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--save", required=True)
    ap.add_argument("--device", default="mps")  # "cuda", "cpu", "mps"
    ap.add_argument("--max-input", type=int, default=384)
    ap.add_argument("--max-new", type=int, default=24)
    args = ap.parse_args()

    device = args.device
    tok = AutoTokenizer.from_pretrained(args.tokenizer, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        args.model, torch_dtype=torch.float16 if device!="cpu" else torch.float32, device_map=None
    )
    model.to(device)

    out = open(args.save, "w", encoding="utf-8")
    with open(args.data, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip(): 
                continue
            row = json.loads(line)
            prompt = pick_prompt(row)

            if isinstance(prompt, list):  # messages
                if hasattr(tok, "apply_chat_template"):
                    text = tok.apply_chat_template(prompt, tokenize=False, add_generation_prompt=True)
                else:
                    # naive fallback if no chat template
                    text = ""
                    for m in prompt:
                        text += f"{m.get('role','user')}: {m.get('content','')}\n"
                    text += "assistant: "
            else:
                text = prompt

            inputs = tok(text, return_tensors="pt", truncation=True, max_length=args.max_input).to(device)
            gen = model.generate(
                **inputs,
                max_new_tokens=args.max_new,
                do_sample=False,
                eos_token_id=tok.eos_token_id,
                pad_token_id=tok.eos_token_id,
                use_cache=True,
            )
            out_text = tok.decode(gen[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)

            out.write(json.dumps({"raw": out_text}, ensure_ascii=False) + "\n")
    out.close()

if __name__ == "__main__":
    main()

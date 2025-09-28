from __future__ import annotations
import os, json, argparse
from dataclasses import dataclass
from typing import List

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from trl import PPOTrainer, PPOConfig, AutoModelForCausalLMWithValueHead

from .prompts import build_train_prompt
from .reward import compute_reward

def pick_device():
    if torch.backends.mps.is_available():
        return "mps"
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"

@dataclass
class Example:
    query: str
    steps: List[str]
    agent: str
    step: int

def load_jsonl(path: str) -> List[Example]:
    rows = []
    with open(path) as f:
        for line in f:
            r = json.loads(line)
            rows.append(Example(
                query=r.get("query",""),
                steps=r.get("steps", []),
                agent=r["label"]["agent"],
                step=int(r["label"]["step"])
            ))
    return rows

def collate_texts(batch: List[Example]):
    return [build_train_prompt(e.query, e.steps) for e in batch]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)  # e.g. Qwen/Qwen2.5-1.5B-Instruct
    ap.add_argument("--train", required=True)
    ap.add_argument("--val", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--batch", type=int, default=1)         # tiny for Mac
    ap.add_argument("--rollouts", type=int, default=1)      # tiny for Mac
    ap.add_argument("--lr", type=float, default=1e-6)
    ap.add_argument("--lam", type=float, default=0.5)
    ap.add_argument("--sigma", type=float, default=1.0)
    ap.add_argument("--max_new_tokens", type=int, default=48)
    ap.add_argument("--epochs", type=int, default=1)
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)

    device = pick_device()
    print(f"[rl_train] using device: {device}")

    tok = AutoTokenizer.from_pretrained(args.model, use_fast=False, trust_remote_code=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token

    base = AutoModelForCausalLM.from_pretrained(
        args.model,
        torch_dtype=torch.float16 if device in ("cuda","mps") else torch.float32,
        device_map="auto",
        trust_remote_code=True,
    )
    model = AutoModelForCausalLMWithValueHead.from_pretrained(base)

    cfg = PPOConfig(
        model_name=args.model,
        learning_rate=args.lr,
        batch_size=args.batch,
        mini_batch_size=1,
        ppo_epochs=1,
        kl_penalty="none"
    )
    trainer = PPOTrainer(config=cfg, model=model, tokenizer=tok)

    train_rows = load_jsonl(args.train)

    for epoch in range(args.epochs):
        for i in range(0, len(train_rows), args.batch):
            batch = train_rows[i:i+args.batch]
            prompts = collate_texts(batch)

            # deterministic generate
            inputs = tok(prompts, return_tensors="pt", padding=True, truncation=True).to(trainer.accelerator.device)
            gen = trainer.generate(
                inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                max_new_tokens=args.max_new_tokens,
                do_sample=False,
                temperature=0.0
            )
            outs = tok.batch_decode(gen, skip_special_tokens=True)

            rewards = []
            for ex, out in zip(batch, outs):
                met = compute_reward(out, ex.agent, ex.step, lam=args.lam, sigma=args.sigma)
                rewards.append(met["R"])

            # PPO step
            q_toks = tok(prompts, return_tensors="pt", padding=True, truncation=True).to(trainer.accelerator.device)
            r_toks = tok(outs,    return_tensors="pt", padding=True, truncation=True).to(trainer.accelerator.device)
            import torch as _torch
            rew = _torch.tensor(rewards, dtype=_torch.float32, device=trainer.accelerator.device)
            trainer.step(list(q_toks["input_ids"]), list(r_toks["input_ids"]), rew)

        save_dir = os.path.join(args.out, f"epoch{epoch:02d}")
        trainer.save_pretrained(save_dir)

if __name__ == "__main__":
    main()

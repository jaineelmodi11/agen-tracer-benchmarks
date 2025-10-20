from dataclasses import dataclass
from typing import List, Dict

import argparse
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from .datasets import JsonlAttributionDataset

PROMPT_USER = "<|user|>\n{}\n<|assistant|>\n"

def build_hf_dataset(path: str):
    ds = JsonlAttributionDataset(path)
    rows = []
    for item in ds:
        rows.append({
            "input_text": PROMPT_USER.format(item["prompt"]),
            "labels": item["target"],
        })
    return Dataset.from_list(rows)

@dataclass
class _label_collator:
    pad_id: int
    def __call__(self, features: List[Dict]):
        import torch
        bs = len(features)
        max_len = max(len(f['input_ids']) for f in features)
        input_ids = torch.full((bs, max_len), self.pad_id, dtype=torch.long)
        attn = torch.zeros((bs, max_len), dtype=torch.long)
        for i,f in enumerate(features):
            ids = torch.tensor(f['input_ids'], dtype=torch.long)
            input_ids[i,:len(ids)] = ids
            attn[i,:len(ids)] = 1
        labels = input_ids.clone()
        labels[labels==self.pad_id] = -100
        return {'input_ids': input_ids, 'attention_mask': attn, 'labels': labels}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--base-model", required=True)
    p.add_argument("--train", required=True)
    p.add_argument("--val",   required=True)
    p.add_argument("--out",   required=True)
    p.add_argument("--lr", type=float, default=2e-4)
    p.add_argument("--epochs", type=int, default=1)
    p.add_argument("--micro-bs", type=int, default=1)
    p.add_argument("--ga-steps", type=int, default=8)
    p.add_argument("--max-len", type=int, default=2048)
    p.add_argument("--lora-r", type=int, default=8)
    p.add_argument("--lora-alpha", type=int, default=16)
    p.add_argument("--lora-dropout", type=float, default=0.05)
    args = p.parse_args()

    tok = AutoTokenizer.from_pretrained(args.base_model, use_fast=True)
    if tok.pad_token_id is None:
        tok.pad_token = tok.eos_token

    model = AutoModelForCausalLM.from_pretrained(args.base_model, torch_dtype="float32")
    model.config.use_cache = False

    # Make it PEFT/LoRA-ready on CPU
    model = prepare_model_for_kbit_training(model)

    # Use "all-linear" so it works across Qwen/Phi without guessing names
    lora = LoraConfig(
        r=args.lora_r,
        lora_alpha=args.lora_alpha,
        lora_dropout=args.lora_dropout,
        target_modules="all-linear",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora)

    train_ds = build_hf_dataset(args.train)
    val_ds   = build_hf_dataset(args.val)

    def tokenize(batch):
        enc = tok(batch["input_text"], truncation=True, max_length=args.max_len)
        lab = tok(text_target=batch["labels"], truncation=True, max_length=args.max_len)
        enc["labels"] = lab["input_ids"]
        return enc

    train_ds = train_ds.map(tokenize, batched=True, remove_columns=train_ds.column_names)
    val_ds   = val_ds.map(tokenize,   batched=True, remove_columns=val_ds.column_names)

    ta = TrainingArguments(
        output_dir=args.out,
        learning_rate=args.lr,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.micro_bs,
        per_device_eval_batch_size=1,
        gradient_accumulation_steps=args.ga_steps,
        logging_steps=25,
        save_steps=200,
        save_total_limit=2,
        bf16=False,
        dataloader_num_workers=0,
        report_to=[],            # no wandb
        use_cpu=True,            # force CPU on Mac
        remove_unused_columns=False,
    )

    collator = _label_collator(pad_id=tok.pad_token_id)

    trainer = Trainer(
        model=model,
        args=ta,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        data_collator=collator,
    )
    trainer.train()
    trainer.save_model(args.out)
    tok.save_pretrained(args.out)

if __name__ == "__main__":
    main()

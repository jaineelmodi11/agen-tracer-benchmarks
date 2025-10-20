#!/usr/bin/env bash
set -euo pipefail

mkdir -p configs data/samples src/atracer scripts checkpoints

# -------- requirements.txt --------
cat > requirements.txt << 'EOF'
transformers>=4.43
accelerate>=0.33
peft>=0.12
datasets>=2.20
scikit-learn>=1.4
numpy>=1.26
ujson>=5.9
rich>=13.7
pydantic>=2.7
# optional serving on Linux; skip on Mac for now
# vllm>=0.5
# sglang>=0.3.7
# fastapi>=0.115
# uvicorn>=0.30
EOF

# -------- sample data --------
cat > data/samples/tiny_demo.jsonl << 'EOF'
{"id":"demo1","query":"Sum list [1,2,'x']","steps":[{"t":0,"agent":"Planner","action":"Break down the task","obs":"Plan created","error":null},{"t":1,"agent":"Coder","action":"Write Python sum","obs":"TypeError: unsupported operand","error":"TypeError"}],"final_status":"fail","label":{"agent":"Coder","step":1}}
{"id":"demo2","query":"Open CSV and compute mean of column A","steps":[{"t":0,"agent":"Web","action":"Download file v1.csv","obs":"200 OK","error":null},{"t":1,"agent":"Analyst","action":"Read column name 'A'","obs":"KeyError: 'A'","error":"KeyError"}],"final_status":"fail","label":{"agent":"Analyst","step":1}}
EOF

# -------- package init --------
cat > src/atracer/__init__.py << 'EOF'
__all__ = []
EOF

# -------- schema.py --------
cat > src/atracer/schema.py << 'EOF'
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class Step(BaseModel):
    t: int
    agent: str
    action: str
    obs: Optional[str] = None
    error: Optional[str] = None

class Record(BaseModel):
    id: str
    query: str
    steps: List[Step]
    final_status: str
    label: Optional[Dict[str, Any]] = None  # {"agent": str, "step": int}
EOF

# -------- prompts.py --------
cat > src/atracer/prompts.py << 'EOF'
from .schema import Record

SYSTEM = (
    "You are a Failure-Attribution Tracer. Given a failed multi-agent trajectory, "
    "identify the EARLIEST decisive error step and the responsible agent at that step.\n"
    "Return only two XML tags: <think>...</think> and <answer>{Agent} | {Step}</answer>."
)

def render_trajectory(rec: Record, max_chars: int = 6000) -> str:
    parts = [f"Task: {rec.query}", "Steps:"]
    for s in rec.steps:
        a = s.action.replace("\n", " ")
        o = (s.obs or "").replace("\n", " ")
        e = s.error or "None"
        parts.append(f"[t={s.t}] agent={s.agent} | action={a} | obs={o} | error={e}")
    text = "\n".join(parts)
    return text[:max_chars]

def build_prompt(rec: Record) -> str:
    traj = render_trajectory(rec)
    instr = (
        "Identify the earliest step whose minimal correction would flip the outcome from FAILURE to SUCCESS.\n"
        "Output strictly in this format:\n<think>...</think>\n<answer>{AgentName} | {StepIndex}</answer>\n"
        "Do not include any extra text."
    )
    return f"{SYSTEM}\n\nTrajectory:\n{traj}\n\n{instr}"
EOF

# -------- parsing.py --------
cat > src/atracer/parsing.py << 'EOF'
import re
from typing import Optional, Tuple

ANS_RE = re.compile(r"<answer>\s*([^|<>]+?)\s*\|\s*(\d+)\s*</answer>", re.IGNORECASE)

def extract_answer(text: str) -> Optional[Tuple[str, int]]:
    m = ANS_RE.search(text)
    if not m:
        return None
    agent = m.group(1).strip()
    step = int(m.group(2))
    return agent, step
EOF

# -------- datasets.py --------
cat > src/atracer/datasets.py << 'EOF'
from typing import Dict, Any, List
import json
from torch.utils.data import Dataset
from .schema import Record, Step
from .prompts import build_prompt

class JsonlAttributionDataset(Dataset):
    def __init__(self, path: str):
        self.records: List[Record] = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                obj = json.loads(line)
                obj["steps"] = [Step(**s) for s in obj["steps"]]
                self.records.append(Record(**obj))

    def __len__(self):
        return len(self.records)

    def __getitem__(self, idx: int) -> Dict[str, Any]:
        rec = self.records[idx]
        prompt = build_prompt(rec)
        target_agent = rec.label["agent"] if rec.label else ""
        target_step = rec.label["step"] if rec.label else -1
        target = f"<think>Reasoning...</think>\n<answer>{target_agent} | {target_step}</answer>"
        return {"prompt": prompt, "target": target, "meta": rec.model_dump()}
EOF

# -------- sft_train.py (Mac-safe; no bitsandbytes) --------
cat > src/atracer/sft_train.py << 'EOF'
import argparse
from dataclasses import dataclass
from datasets import Dataset
from transformers import (
    AutoModelForCausalLM, AutoTokenizer,
    Trainer, TrainingArguments, DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from .datasets import JsonlAttributionDataset

@dataclass
class Args:
    base_model: str
    train: str
    val: str
    out: str
    lr: float = 2e-4
    epochs: int = 2
    micro_bs: int = 1
    ga_steps: int = 16
    max_len: int = 4096
    lora_r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05

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

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--base-model", required=True)
    p.add_argument("--train", required=True)
    p.add_argument("--val", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--lr", type=float, default=2e-4)
    p.add_argument("--epochs", type=int, default=2)
    p.add_argument("--micro-bs", type=int, default=1)
    p.add_argument("--ga-steps", type=int, default=16)
    p.add_argument("--max-len", type=int, default=4096)
    p.add_argument("--lora-r", type=int, default=16)
    p.add_argument("--lora-alpha", type=int, default=32)
    p.add_argument("--lora-dropout", type=float, default=0.05)
    args = p.parse_args()

    tok = AutoTokenizer.from_pretrained(args.base_model, use_fast=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        args.base_model,
        torch_dtype="auto",
        device_map="auto",
    )

    model = prepare_model_for_kbit_training(model)
    lora = LoraConfig(
        r=args.lora_r, lora_alpha=args.lora_alpha, lora_dropout=args.lora_dropout,
        target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"],
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora)

    train_ds = build_hf_dataset(args.train)
    val_ds = build_hf_dataset(args.val)

    def tokenize(batch):
        enc = tok(batch["input_text"], truncation=True, max_length=args.max_len)
        with tok.as_target_tokenizer():
            lab = tok(batch["labels"], truncation=True, max_length=args.max_len)
        enc["labels"] = lab["input_ids"]
        return enc

    train_ds = train_ds.map(tokenize, batched=True, remove_columns=train_ds.column_names)
    val_ds = val_ds.map(tokenize, batched=True, remove_columns=val_ds.column_names)

    collator = DataCollatorForLanguageModeling(tok, mlm=False)

    ta = TrainingArguments(
        output_dir=args.out,
        learning_rate=args.lr,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.micro_bs,
        per_device_eval_batch_size=1,
        gradient_accumulation_steps=args.ga_steps,
        evaluation_strategy="steps",
        eval_steps=50,
        logging_steps=25,
        save_steps=200,
        save_total_limit=2,
        bf16=False,
        dataloader_num_workers=0,
        report_to=[],
    )

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
EOF

# -------- infer.py --------
cat > src/atracer/infer.py << 'EOF'
import argparse, json
from transformers import AutoModelForCausalLM, AutoTokenizer
from .schema import Record
from .prompts import build_prompt
from .parsing import extract_answer

PROMPT_USER = "<|user|>\n{}\n<|assistant|>\n"

def gen(model_path: str, text: str, max_new_tokens=256):
    tok = AutoTokenizer.from_pretrained(model_path, use_fast=True)
    model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto")
    ids = tok(PROMPT_USER.format(text), return_tensors="pt").to(model.device)
    out = model.generate(**ids, max_new_tokens=max_new_tokens)
    return tok.decode(out[0], skip_special_tokens=True)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True)
    p.add_argument("--jsonl", required=True)
    args = p.parse_args()

    with open(args.jsonl, "r", encoding="utf-8") as f:
        for line in f:
            rec = Record(**json.loads(line))
            prompt = build_prompt(rec)
            text = gen(args.model, prompt)
            ans = extract_answer(text) or (None, None)
            print(rec.id, "->", ans, "\nRAW:\n", text)
EOF

# -------- eval.py --------
cat > src/atracer/eval.py << 'EOF'
import argparse, json
from transformers import AutoModelForCausalLM, AutoTokenizer
from .schema import Record
from .prompts import build_prompt
from .parsing import extract_answer

PROMPT_USER = "<|user|>\n{}\n<|assistant|>\n"

def infer_one(model, tok, prompt: str, max_new_tokens=256):
    ids = tok(PROMPT_USER.format(prompt), return_tensors="pt").to(model.device)
    out = model.generate(**ids, max_new_tokens=max_new_tokens)
    return tok.decode(out[0], skip_special_tokens=True)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True)
    p.add_argument("--data", required=True)
    args = p.parse_args()

    tok = AutoTokenizer.from_pretrained(args.model, use_fast=True)
    model = AutoModelForCausalLM.from_pretrained(args.model, device_map="auto")

    n = 0
    agent_ok = 0
    step_ok = 0
    both_ok = 0

    with open(args.data, "r", encoding="utf-8") as f:
        for line in f:
            rec = Record(**json.loads(line))
            gold_a = rec.label["agent"]
            gold_t = rec.label["step"]
            prompt = build_prompt(rec)
            text = infer_one(model, tok, prompt)
            pred = extract_answer(text)
            if pred is None:
                n += 1
                continue
            pa, pt = pred
            n += 1
            a_ok = (pa.strip().lower() == gold_a.strip().lower())
            t_ok = (pt == gold_t)
            agent_ok += int(a_ok)
            step_ok += int(t_ok)
            both_ok += int(a_ok and t_ok)

    print({
        "samples": n,
        "agent_acc": agent_ok / max(1, n),
        "step_acc": step_ok / max(1, n),
        "both_acc": both_ok / max(1, n),
    })
EOF

# -------- helper: render_traj_text.py --------
cat > scripts/render_traj_text.py << 'EOF'
# Preview how a JSONL record renders into the training prompt
import json, argparse
from src.atracer.schema import Record
from src.atracer.prompts import build_prompt

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--jsonl", required=True)
    p.add_argument("--n", type=int, default=1)
    args = p.parse_args()
    with open(args.jsonl, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= args.n: break
            rec = Record(**json.loads(line))
            print(build_prompt(rec))
EOF

# -------- who_when prep (later) --------
cat > scripts/prepare_who_when.py << 'EOF'
"""
Map your raw Who&When-style JSON into our jsonl schema (train/val).
Adjust field names to your raw file.
"""
import argparse, json, random
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out-prefix", required=True)
    ap.add_argument("--val-ratio", type=float, default=0.2)
    args = ap.parse_args()

    with open(args.inp, "r", encoding="utf-8") as f:
        raw = json.load(f)

    rows = []
    for ex in raw:
        steps = []
        for t, st in enumerate(ex.get("trajectory", [])):
            steps.append({
                "t": t,
                "agent": st.get("agent", "Agent"),
                "action": st.get("action", ""),
                "obs": st.get("obs", ""),
                "error": st.get("error", None)
            })
        rows.append({
            "id": ex.get("id", f"ex_{len(rows)}"),
            "query": ex.get("query", ""),
            "steps": steps,
            "final_status": ex.get("final_status", "fail"),
            "label": {"agent": ex["label"]["agent"], "step": int(ex["label"]["step"])},
        })

    random.shuffle(rows)
    n_val = int(len(rows) * args.val_ratio)
    val = rows[:n_val]; train = rows[n_val:]

    out_tr = Path(args.out_prefix + ".train.jsonl")
    out_va = Path(args.out_prefix + ".val.jsonl")
    with out_tr.open("w", encoding="utf-8") as f:
        for r in train:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with out_va.open("w", encoding="utf-8") as f:
        for r in val:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main()
EOF

echo "✅ Files created."

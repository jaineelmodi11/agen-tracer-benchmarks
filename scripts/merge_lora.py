import os, tempfile, argparse, torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# keep things simple & CPU-only
os.environ["ACCELERATE_DISABLE_MIXED_PRECISION"] = "1"

p = argparse.ArgumentParser()
p.add_argument("--base", required=True)
p.add_argument("--adapter", required=True)
p.add_argument("--out", required=True)
args = p.parse_args()

print("Loading base on CPU:", args.base)
base = AutoModelForCausalLM.from_pretrained(
    args.base,
    torch_dtype=torch.float32,
    device_map={"": "cpu"},
    low_cpu_mem_usage=True,   # <-- REQUIRED when using device_map
)

offload_dir = tempfile.mkdtemp(prefix="peft-offload-")
print("Loading adapter on CPU:", args.adapter)
model = PeftModel.from_pretrained(
    base,
    args.adapter,
    device_map={"": "cpu"},
    offload_folder=offload_dir,
)

print("Merging LoRA into base…")
merged = model.merge_and_unload()

print("Saving merged model to:", args.out)
os.makedirs(args.out, exist_ok=True)
tok = AutoTokenizer.from_pretrained(args.base, use_fast=True)
merged.save_pretrained(args.out, safe_serialization=True)
tok.save_pretrained(args.out)
print("✅ Done. Merged model is at:", args.out)

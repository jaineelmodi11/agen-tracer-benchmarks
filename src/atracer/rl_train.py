from __future__ import annotations

# --- Prefer MPS on macOS; keep CUDA optional ---
import os as _os
_os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")
_os.environ.setdefault("ACCELERATE_USE_MPS_DEVICE", "1")
# ------------------------------------------------

import os
import sys
import json
import argparse
import random
from dataclasses import dataclass
from typing import List

import torch
from packaging import version as _v
from transformers import AutoTokenizer, AutoModelForCausalLM

# TRL imports (targeting 0.9.x)
try:
    import trl
    from trl import PPOTrainer, PPOConfig, AutoModelForCausalLMWithValueHead
except Exception as e:
    print(f"[rl_train] ERROR: Could not import TRL: {e}", file=sys.stderr)
    raise


def pick_device() -> str:
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
    rows: List[Example] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            r = json.loads(s)
            label = r.get("label") or {}
            rows.append(Example(
                query=r.get("query", ""),
                steps=r.get("steps", []),
                agent=(label.get("agent", r.get("agent", "")) or ""),
                step=int(label.get("step", r.get("step", 0))),
            ))
    return rows


def build_prompt(query: str, steps: List[str], *, builder):
    return builder(query, steps)


def main():
    ap = argparse.ArgumentParser(
        description="RL fine-tuning for failure attribution head (PPO, TRL 0.9.x expected)."
    )
    ap.add_argument("--model", required=True, help="Policy init (HF hub id or local dir with weights).")
    ap.add_argument("--tokenizer", default=None, help="Tokenizer source (HF id). If omitted, use --model.")
    ap.add_argument("--train", required=True, help="Training jsonl (expects label.agent/label.step).")
    ap.add_argument("--val", required=True, help="(unused placeholder).")
    ap.add_argument("--out", required=True, help="Output directory to save checkpoints.")

    # small-device-friendly defaults
    ap.add_argument("--batch", type=int, default=1, help="Batch size per PPO update.")
    ap.add_argument("--lr", type=float, default=1e-6, help="Learning rate.")
    ap.add_argument("--ppo-epochs", type=int, default=2, help="Number of PPO epochs (reduce for MPS).")
    ap.add_argument("--dtype", choices=["auto", "float16", "float32"], default="auto",
                    help="Compute dtype for policy/ref forwards.")
    ap.add_argument("--max_new_tokens", type=int, default=24, help="Max generation length for answers.")
    ap.add_argument("--max_prompt_tokens", type=int, default=384, help="Max encoded prompt tokens (left-truncated).")

    # Control total update steps by dataset cycling
    ap.add_argument("--updates", type=int, default=32, help="Total PPO updates to run (dataset will cycle).")
    ap.add_argument("--save-every", type=int, default=8, help="Save every N updates.")

    # Reward weights
    ap.add_argument("--lam", type=float, default=0.8, help="step reward weight (beta).")
    ap.add_argument("--sigma", type=float, default=0.8, help="agent reward weight (gamma).")
    ap.add_argument("--alpha", type=float, default=1.0, help="format gate penalty magnitude.")
    ap.add_argument("--warmup-updates", type=int, default=8,
                    help="curriculum: for the first K updates, set beta=0 (agent-first).")

    # Memory knobs
    ap.add_argument("--no-grad-checkpoint", action="store_true",
                    help="Disable gradient checkpointing (enabled by default).")

    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    # -----------------
    # TRL version gate
    # -----------------
    try:
        trl_ver = _v.parse(trl.__version__)
    except Exception:
        trl_ver = _v.parse("0")
    print(f"[rl_train] detected TRL {trl.__version__}")
    if trl_ver >= _v.parse("0.23.0"):
        print(
            f"[rl_train] ERROR: TRL {trl.__version__} detected. "
            "This script targets TRL 0.9.x (classic PPO API).\n"
            "Install a compatible stack and re-run:\n"
            "  pip install --upgrade 'trl==0.9.6' 'transformers==4.44.2' 'accelerate==0.33.0' 'tokenizers==0.19.1'\n",
            file=sys.stderr,
        )
        sys.exit(2)

    from .prompts import build_train_prompt
    from .reward import compute_reward

    # -----------------
    # Devices / seeds
    # -----------------
    device_str = pick_device()
    dev = torch.device("mps" if device_str == "mps" else ("cuda" if device_str == "cuda" else "cpu"))
    torch.manual_seed(42)
    random.seed(42)
    print(f"[rl_train] using device: {device_str}")
    print(f"[rl_train] tokenizer source: {args.tokenizer or args.model}")

    # -----------------
    # Tokenizer / model
    # -----------------
    tok_src = args.tokenizer or args.model
    tok = AutoTokenizer.from_pretrained(tok_src, use_fast=False, trust_remote_code=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    tok.truncation_side = "left"
    tok.padding_side = "left"

    # Dtype (use fp16 on MPS/CUDA by default to save memory)
    if args.dtype == "auto":
        dtype = torch.float16 if device_str in ("cuda", "mps") else torch.float32
    elif args.dtype == "float16":
        dtype = torch.float16
    else:
        dtype = torch.float32

    # Policy (trainable)
    base = AutoModelForCausalLM.from_pretrained(
        args.model,
        torch_dtype=dtype,
        device_map=None,
        trust_remote_code=True,
    )
    model = AutoModelForCausalLMWithValueHead.from_pretrained(base)
    model.pretrained_model.to(dev)
    if hasattr(model, "v_head"):
        model.v_head.to(dev)

    # Reference (frozen)
    ref_base = AutoModelForCausalLM.from_pretrained(
        args.model,
        torch_dtype=dtype,
        device_map=None,
        trust_remote_code=True,
    )
    ref_model = AutoModelForCausalLMWithValueHead.from_pretrained(ref_base)
    ref_model.pretrained_model.to(dev)
    if hasattr(ref_model, "v_head"):
        ref_model.v_head.to(dev)
    for p in ref_model.parameters():
        p.requires_grad_(False)
    ref_model.eval()

    # Memory savers
    if not args.no_grad_checkpoint:
        # Enable gradient checkpointing on the trainable policy
        if hasattr(model.pretrained_model, "gradient_checkpointing_enable"):
            model.pretrained_model.gradient_checkpointing_enable()
        # Disable KV cache during training forward to reduce memory
        try:
            model.pretrained_model.config.use_cache = False
        except Exception:
            pass
    # Also disable cache on the ref model (no grads, but still saves memory)
    try:
        ref_model.pretrained_model.config.use_cache = False
    except Exception:
        pass

    # -----------
    # PPO config  (TRL 0.9.x)
    # -----------
    cfg = PPOConfig(
        seed=42,
        learning_rate=args.lr,
        batch_size=args.batch,
        mini_batch_size=1,                 # safe on Macs
        ppo_epochs=int(args.ppo_epochs),   # fewer epochs => lower peak mem
        cliprange=0.2,
        cliprange_value=0.2,
        target_kl=0.1,
        kl_penalty="kl",
        init_kl_coef=0.05,
        vf_coef=0.1,
        gamma=1.0,
        lam=0.95,
    )

    trainer = PPOTrainer(
        config=cfg,
        model=model,
        ref_model=ref_model,
        tokenizer=tok,
    )

    # Generation defaults for PPO rollouts (sampling ON)
    gen_kwargs = dict(
        max_new_tokens=args.max_new_tokens,
        do_sample=True,
        temperature=1.0,
        top_p=0.95,
        top_k=50,
        eos_token_id=tok.eos_token_id,
        pad_token_id=tok.pad_token_id,
        use_cache=True,  # cache is fine for generation; we only disable it on training forwards
        repetition_penalty=1.05,
        no_repeat_ngram_size=3,
    )

    # ----------
    # Data load
    # ----------
    train_rows = load_jsonl(args.train)
    if not train_rows:
        raise SystemExit(f"No rows found in {args.train}")
    N = len(train_rows)
    if args.batch < 1:
        raise SystemExit("--batch must be >= 1")

    print(f"[rl_train] train rows = {N} | target updates = {args.updates} | batch = {args.batch}")

    # ------------------------------
    # Main loop: generate -> reward
    # ------------------------------
    updates_done = 0
    i_ptr = 0  # dataset cursor

    while updates_done < args.updates:
        # slice a batch (cycle dataset)
        batch_examples: List[Example] = []
        need = args.batch
        while need > 0:
            take = min(need, N - i_ptr)
            if take == 0:
                i_ptr = 0
                continue
            batch_examples.extend(train_rows[i_ptr:i_ptr + take])
            i_ptr += take
            need -= take
            if i_ptr >= N:
                i_ptr = 0

        # Build prompts (train-format)
        from .prompts import build_train_prompt
        prompts = [build_prompt(ex.query, ex.steps, builder=build_train_prompt) for ex in batch_examples]

        # Encode individually (left-truncated)
        queries = [
            tok(
                p,
                return_tensors="pt",
                truncation=True,
                max_length=args.max_prompt_tokens,
                add_special_tokens=True,
            )["input_ids"].squeeze(0).to(dev)
            for p in prompts
        ]

        # Rollout
        response_tensors = trainer.generate(queries, **gen_kwargs)

        # Decode continuations for reward shaping
        texts: List[str] = [tok.decode(r, skip_special_tokens=True) for r in response_tensors]

        # Curriculum: agent-first for first K updates (beta=0)
        beta_now = 0.0 if updates_done < args.warmup_updates else args.lam
        if updates_done == args.warmup_updates:
            print(f"[rl_train] curriculum switch: enabling step weight beta={args.lam}")

        # Compute scalar rewards
        from .reward import compute_reward
        rewards: List[torch.Tensor] = []
        for ex, out_text in zip(batch_examples, texts):
            met = compute_reward(
                out_text,
                ex.agent,
                ex.step,
                alpha=args.alpha,    # format gate
                beta=beta_now,       # step weight (0 during warmup)
                gamma=args.sigma,    # agent weight
            )
            R = float(met.get("R", 0.0))
            if not (R == R) or R in (float("inf"), float("-inf")):
                R = -0.2  # guard against NaNs/Infs
            rewards.append(torch.tensor(R, dtype=torch.float32, device=dev))

        # PPO update
        stats = trainer.step(queries, response_tensors, rewards)

        # Optional stabilization if KL looks odd
        kl = float(stats.get("objective/kl", 0.0))
        if kl < -0.01 or abs(kl) > 1.0:
            print(f"[warn] odd KL={kl:.3f} -> increasing kl_coef, lowering lr")
            try:
                trainer.kl_ctl.value *= 1.5
            except Exception:
                pass
            for g in trainer.optimizer.param_groups:
                g["lr"] = max(g["lr"] * 0.5, 2e-7)

        updates_done += 1

        # Proactively free MPS memory between iterations
        if torch.backends.mps.is_available():
            try:
                torch.mps.empty_cache()
            except Exception:
                pass

        # Periodic save
        if (updates_done % max(1, args.save_every)) == 0:
            save_dir = os.path.join(args.out, f"epoch00-upd{updates_done:03d}")
            os.makedirs(save_dir, exist_ok=True)
            trainer.model.pretrained_model.save_pretrained(save_dir)
            tok.save_pretrained(save_dir)
            print(f"[rl_train] saved policy to {save_dir}")

    # Final save
    final_dir = os.path.join(args.out, "epoch00-final")
    os.makedirs(final_dir, exist_ok=True)
    trainer.model.pretrained_model.save_pretrained(final_dir)
    tok.save_pretrained(final_dir)
    print(f"[rl_train] saved epoch-end policy to {final_dir}")


if __name__ == "__main__":
    main()

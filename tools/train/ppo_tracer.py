from __future__ import annotations
import os, sys
os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")

import argparse, json, re, inspect, random, csv, math
from typing import List, Dict, Optional, Iterable

THIS_DIR = os.path.dirname(__file__)
REPO_ROOT = os.path.abspath(os.path.join(THIS_DIR, "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import torch
from datasets import Dataset
from transformers import AutoTokenizer, LogitsProcessorList, StoppingCriteriaList
from trl import PPOConfig, PPOTrainer, AutoModelForCausalLMWithValueHead

from src.atracer.rewards import compute_reward
from src.atracer.prompts import build_eval_prompt
from src.atracer.logit_tools import (
    FirstTokenRestrictor,
    StepDigitRestrictor,
    StopOnFirstPair,
    build_agent_token_map,
    PAIR_RE,
    # safer step gate:
    AgentThenStepRestrictor,
)

# NEW: tracer head (WHO/WHEN) aux loss
try:
    from src.atracer.tracer_head import TracerHead
except Exception:
    TracerHead = None  # we'll guard below


# ---------------- small utils ----------------

def _scrub_gen_cfg(m):
    try:
        base = getattr(m, "pretrained_model", m)
        gc = getattr(base, "generation_config", None)
        if gc is not None:
            for k in ("temperature", "top_p", "top_k", "typical_p", "penalty_alpha"):
                if hasattr(gc, k):
                    setattr(gc, k, None)
            if hasattr(gc, "do_sample"):
                gc.do_sample = False
    except Exception:
        pass

def _score_prompt_is_codey(prompt: str) -> float:
    needles = [
        r"```", r"\bdef\b", r"\bclass\b", r"\bimport\b", r"\breturn\b", r"\bfunction\b",
        r"\btraceback\b", r"\bstack\s*trace\b", r"\berror:\b", r"\bcompile\b",
        r"\bunit\s*test\b", r"\bpytest\b", r"\bassert\b",
    ]
    hits = sum(bool(re.search(rx, prompt, re.I)) for rx in needles)
    return min(1.0, hits / 4.0)

def _load_jsonl(path: str):
    out = []
    with open(path, encoding="utf-8") as f:
        for ln in f:
            if ln.strip():
                out.append(json.loads(ln))
    return out

def _ppo_config_from_args(args) -> PPOConfig:
    cfg = PPOConfig()
    def _set(name, value):
        if hasattr(cfg, name):
            setattr(cfg, name, value)
    _set("learning_rate", args.lr)
    _set("batch_size", args.batch_size)
    if hasattr(cfg, "mini_batch_size"):
        _set("mini_batch_size", args.mini_batch_size)
    elif hasattr(cfg, "forward_batch_size"):
        _set("forward_batch_size", args.mini_batch_size)
    for k in ("ppo_epochs", "num_ppo_epochs", "epochs"):
        if hasattr(cfg, k):
            setattr(cfg, k, args.epochs)
            break
    _set("target_kl", args.kl_coef)
    _set("cliprange", args.cliprange)
    _set("remove_unused_columns", False)
    _set("ratio_threshold", args.ratio_threshold)
    _set("forward_batch_size", args.forward_batch_size)
    return cfg

def _build_trainer(ppo_cfg, model, tok, ds_train):
    sig = inspect.signature(PPOTrainer.__init__)
    params = list(sig.parameters.keys())[1:]
    kwargs, args = {}, []
    if len(params) > 0 and params[0] in ("config", "ppo_config"):
        pass
    else:
        args.append(ppo_cfg)
    if "config" in params: kwargs["config"] = ppo_cfg
    if "ppo_config" in params: kwargs["ppo_config"] = ppo_cfg
    if "model" in params: kwargs["model"] = model
    if "ref_model" in params: kwargs["ref_model"] = None
    if "tokenizer" in params: kwargs["tokenizer"] = tok
    if "dataset" in params: kwargs["dataset"] = ds_train
    if "train_dataset" in params: kwargs["train_dataset"] = ds_train
    if "data_collator" in params: kwargs["data_collator"] = None
    if "reward_model" in params: kwargs["reward_model"] = None
    if "value_model" in params: kwargs["value_model"] = None
    return PPOTrainer(*args, **kwargs)

def _make_loader(ds_train, batch_size: int):
    from torch.utils.data import DataLoader
    def _collate(batch):
        out = {"prompt": [], "gold_agent": [], "gold_step": [], "n_steps": []}
        for b in batch:
            out["prompt"].append(b["prompt"])
            out["gold_agent"].append(b["gold_agent"])
            out["gold_step"].append(b["gold_step"])
            out["n_steps"].append(int(b.get("n_steps", 1)))
        return out
    return DataLoader(ds_train, batch_size=batch_size, shuffle=True, collate_fn=_collate)

def _parse_first_pair(text: str, allowed: Iterable[str]) -> Optional[tuple[str,int]]:
    for mm in PAIR_RE.finditer(text or ""):
        a = mm.group(1).lower()
        if not allowed or a in allowed:
            try:
                return a, int(mm.group(2))
            except Exception:
                return None
    return None

class _CSVLogger:
    def __init__(self, path: Optional[str]):
        self.path = path
        self._header_written = False
        if path:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            if os.path.exists(path):
                self._header_written = True
    def log(self, **kw):
        if not self.path:
            return
        with open(self.path, "a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=sorted(kw.keys()))
            if not self._header_written:
                w.writeheader()
                self._header_written = True
            w.writerow(kw)


# ---------------- main ----------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", required=True)
    ap.add_argument("--val", required=True)
    ap.add_argument("--save_dir", required=True)

    ap.add_argument("--model", required=True)
    ap.add_argument("--tokenizer", required=True)

    ap.add_argument("--device", default="")
    ap.add_argument("--max_input", type=int, default=384)
    ap.add_argument("--max_new", type=int, default=16)

    ap.add_argument("--allowed_agents", default="analyst,coder")

    # compute_reward weights
    ap.add_argument("--w_parse", type=float, default=0.6)
    ap.add_argument("--w_agent", type=float, default=2.0)
    ap.add_argument("--w_step_exact", type=float, default=0.5)
    ap.add_argument("--w_step_close", type=float, default=0.05)
    ap.add_argument("--close_tol", type=int, default=1)
    ap.add_argument("--w_len", type=float, default=-0.004)

    # PPO knobs
    ap.add_argument("--passes", type=int, default=1)
    ap.add_argument("--batch_size", type=int, default=64)
    ap.add_argument("--mini_batch_size", type=int, default=16)
    ap.add_argument("--epochs", type=int, default=1)
    ap.add_argument("--lr", type=float, default=5e-6)
    ap.add_argument("--cliprange", type=float, default=0.15)
    ap.add_argument("--kl_coef", type=float, default=0.1)
    ap.add_argument("--ratio_threshold", type=float, default=1e5)
    ap.add_argument("--forward_batch_size", type=int, default=1)

    # gating & CFR
    ap.add_argument("--step_gate", choices=["off", "eager", "safe"], default="safe",
                    help="off: none; eager: StepDigitRestrictor; safe: AgentThenStepRestrictor")
    ap.add_argument("--cfr_prob", type=float, default=0.0,
                    help="probability to add a counterfactual replay item for each mistake (0 disables)")
    ap.add_argument("--cfr_max_per_batch", type=int, default=8)
    ap.add_argument("--cfr_reward", type=float, default=1.0)

    # NEW: tracer aux loss + metrics
    ap.add_argument("--enable_tracer", action="store_true",
                    help="enable WHO/WHEN tracer loss as auxiliary objective")
    ap.add_argument("--tracer_hidden", type=int, default=1024)
    ap.add_argument("--tracer_n_when", type=int, default=33,  # 32 steps + 'no-fail'
                    help="number of WHEN classes (max steps + 1 for 'no-fail')")
    ap.add_argument("--lambda_tracer", type=float, default=0.1,
                    help="weight on tracer aux loss")
    ap.add_argument("--log_csv", type=str, default="run/logs/train.csv",
                    help="optional CSV log path (metrics)")

    args = ap.parse_args()
    device = args.device or ("mps" if torch.backends.mps.is_available()
                             else "cuda" if torch.cuda.is_available()
                             else "cpu")

    logger = _CSVLogger(args.log_csv if args.log_csv else None)

    tok = AutoTokenizer.from_pretrained(args.tokenizer, trust_remote_code=True)
    tok.truncation_side = "left"
    tok.padding_side = "left"
    if tok.pad_token_id is None:
        tok.pad_token = tok.eos_token

    model = AutoModelForCausalLMWithValueHead.from_pretrained(
        args.model, trust_remote_code=True
    ).to(device)
    _scrub_gen_cfg(model)

    try:
        model.config.use_cache = False
        base = getattr(model, "pretrained_model", None)
        if base is not None:
            base.config.use_cache = False
            if hasattr(base, "gradient_checkpointing_enable"):
                base.gradient_checkpointing_enable()
    except Exception:
        pass

    # dataset -> {prompt, gold_agent, gold_step, n_steps}
    def _to_rows(path):
        raw = _load_jsonl(path)
        out = []
        for r in raw:
            q = (r.get("query") or r.get("instruction") or r.get("prompt") or r.get("input") or "")
            steps = r.get("steps") or r.get("trace") or r.get("rationale") or []
            lab = r.get("label") or {}
            if not q or not steps or "agent" not in lab or "step" not in lab:
                continue
            prompt = build_eval_prompt(q, steps)
            out.append({
                "prompt": prompt,
                "gold_agent": lab["agent"],
                "gold_step": int(lab["step"]),
                "n_steps": int(len(steps)),
            })
        return out

    train_rows = _to_rows(args.train)
    if len(train_rows) == 0:
        raise RuntimeError(f"No valid training rows found in {args.train}")
    ds_train = Dataset.from_list(train_rows)

    ppo_cfg = _ppo_config_from_args(args)
    ppo = _build_trainer(ppo_cfg, model, tok, ds_train)
    loader = _make_loader(ds_train, args.batch_size)

    # agent biasing
    allowed = [x.strip().lower() for x in (args.allowed_agents or "").split(",") if x.strip()]
    agent_token_map = build_agent_token_map(tok, allowed) if allowed else {}
    agent_start_ids_union = set()
    for a in allowed:
        for tid in agent_token_map.get(a, []):
            agent_start_ids_union.add(tid)

    # WHO label mapping (binary)
    # 0 => analyst, 1 => coder  (if agent not in set, default to coder)
    def _who_label(agent: str) -> int:
        agent = (agent or "").strip().lower()
        if agent == "analyst": return 0
        if agent == "coder":   return 1
        # default: treat as coder
        return 1

    # tracer head + optimizer
    tracer = None
    tracer_optim = None
    if args.enable_tracer:
        if TracerHead is None:
            raise RuntimeError("TracerHead not found. Ensure src/atracer/tracer_head.py is present and importable.")
        tracer = TracerHead(hidden_size=args.tracer_hidden, n_when_classes=args.tracer_n_when).to(device)
        tracer_optim = torch.optim.AdamW(tracer.parameters(), lr=1e-4)

    rng = random.Random(42)

    step_idx = 0
    for _ in range(max(1, args.passes)):
        for batch in loader:
            prompts: List[str] = batch["prompt"]
            gold_agents: List[str] = batch["gold_agent"]
            gold_steps: List[int] = batch["gold_step"]
            n_steps_list: List[int] = batch["n_steps"]

            enc = tok(
                prompts, return_tensors="pt", padding=True, truncation=True, max_length=args.max_input
            ).to(device)
            input_ids = enc["input_ids"]
            attention_mask = enc["attention_mask"]

            responses_list: List[torch.LongTensor] = []
            conts: List[str] = []

            # ---------- generate ----------
            for i in range(input_ids.size(0)):
                q_ids = input_ids[i].unsqueeze(0)
                q_mask = attention_mask[i].unsqueeze(0)
                prompt_len = q_ids.shape[1]

                prior = {}
                if allowed:
                    codeyness = _score_prompt_is_codey(prompts[i])
                    coder_boost = 2.0 * codeyness
                    analyst_boost = 1.2 * (1.0 - codeyness)
                    for tid in agent_token_map.get("coder", []):
                        prior[tid] = prior.get(tid, 0.0) + coder_boost
                    for tid in agent_token_map.get("analyst", []):
                        prior[tid] = prior.get(tid, 0.0) + analyst_boost

                procs = LogitsProcessorList()
                if allowed:
                    procs.append(
                        FirstTokenRestrictor(
                            prompt_len=prompt_len,
                            tok=tok,
                            allowed_agents=allowed,
                            agent_token_map=agent_token_map,
                            bias=prior,
                        )
                    )
                # Step gate
                if args.step_gate == "eager":
                    procs.append(StepDigitRestrictor(prompt_len=prompt_len, tok=tok, n_steps=int(n_steps_list[i])))
                elif args.step_gate == "safe":
                    procs.append(AgentThenStepRestrictor(
                        prompt_len=prompt_len,
                        tok=tok,
                        agent_start_ids=agent_start_ids_union,
                        n_steps=int(n_steps_list[i]),
                    ))

                stops = StoppingCriteriaList([StopOnFirstPair(tok, prompt_len, allowed=allowed)])

                out = ppo.model.generate(
                    input_ids=q_ids,
                    attention_mask=q_mask,
                    max_new_tokens=args.max_new,
                    min_new_tokens=1,
                    do_sample=False,
                    temperature=None, top_p=None, top_k=None, typical_p=None, penalty_alpha=None,
                    logits_processor=procs if len(procs) > 0 else None,
                    stopping_criteria=stops,
                    pad_token_id=tok.pad_token_id,
                    eos_token_id=tok.eos_token_id,
                    return_dict_in_generate=True,
                )
                seq = out.sequences[0]
                r = seq[prompt_len:].contiguous()
                cont_text = tok.decode(r.tolist(), skip_special_tokens=True)

                if not PAIR_RE.search(cont_text):
                    cont_text = "Analyst 1"
                    r = torch.tensor(
                        tok.encode(" Analyst 1", add_special_tokens=False),
                        device=device, dtype=torch.long
                    )

                responses_list.append(r)
                conts.append(cont_text)

            queries_list = [q for q in input_ids]

            # ---------- reward ----------
            rewards: List[float] = []
            for pred, ga, gs in zip(conts, gold_agents, gold_steps):
                R = compute_reward(
                    pred,
                    gold_agent=ga,
                    gold_step=int(gs),
                    allowed_agents=allowed,
                    pick="first",
                    w_parse=args.w_parse,
                    w_agent=args.w_agent,
                    w_step_exact=args.w_step_exact,
                    w_step_close=args.w_step_close,
                    close_tol=args.close_tol,
                    w_len=args.w_len,
                )["R"]
                rewards.append(float(R))

            scores_list = [torch.tensor(R, device=device, dtype=torch.float32) for R in rewards]

            # ---------- PPO step ----------
            try:
                ppo.step(queries_list, responses_list, scores_list)
            except Exception as e:
                msg = str(e)
                if "expected a non-empty list of Tensors" in msg or "empty internal batch" in msg:
                    print("[skip] TRL produced an empty internal batch; continuing.")
                else:
                    raise

            # ---------- tracer aux update (WHO/WHEN) ----------
            tracer_loss_val = None
            who_acc = None
            when_acc = None
            joint_acc = None

            if tracer is not None:
                # Build a small batch of (q + response) so gradients can flow into the LM
                full_ids = []
                full_masks = []
                who_labels = []
                when_labels = []
                for i, (q_ids, r_ids, ga, gs) in enumerate(zip(input_ids, responses_list, gold_agents, gold_steps)):
                    r_ids = r_ids.detach()  # as tokens chosen
                    seq = torch.cat([q_ids, r_ids], dim=0)  # [Tq + Tr]
                    full_ids.append(seq)
                    full_masks.append(torch.ones_like(seq))
                    who_labels.append(_who_label(ga))
                    # WHEN: clamp into [0, tracer_n_when-1]
                    when_labels.append(int(gs) if int(gs) < args.tracer_n_when else args.tracer_n_when - 1)

                # pad to max length in the micro-batch
                maxlen = max(x.shape[0] for x in full_ids)
                pad_id = tok.pad_token_id
                full_ids = torch.stack([torch.cat([x, torch.full((maxlen - x.shape[0],), pad_id, device=device, dtype=torch.long)]) for x in full_ids])
                full_masks = torch.stack([torch.cat([m, torch.zeros((maxlen - m.shape[0],), device=device, dtype=torch.long)]) for m in full_masks])

                # forward through base to get hidden states
                base = getattr(ppo.model, "pretrained_model", ppo.model)
                out = base(input_ids=full_ids, attention_mask=full_masks, output_hidden_states=True)
                last_h = out.hidden_states[-1]              # [B, T, H]
                # pool over the response span ONLY (q_len..end); approximate by masking out left padding + prompt tokens
                # we don't have per-sample prompt length here, so mean-pool over all unpadded tokens (good enough)
                mask = full_masks.unsqueeze(-1).float()     # [B, T, 1]
                denom = mask.sum(dim=1).clamp_min(1.0)      # [B, 1]
                pooled = (last_h * mask).sum(dim=1) / denom # [B, H]

                who_t = torch.tensor(who_labels, device=device, dtype=torch.long)
                when_t = torch.tensor(when_labels, device=device, dtype=torch.long)

                t_out = tracer(pooled, who_labels=who_t, when_labels=when_t)
                tracer_loss = t_out.loss if t_out.loss is not None else None

                # metrics
                with torch.no_grad():
                    wp = t_out.who_logits.argmax(dim=-1)
                    tp = t_out.when_logits.argmax(dim=-1)
                    who_acc = float((wp == who_t).float().mean().item())
                    when_acc = float((tp == when_t).float().mean().item())
                    joint_acc = float(((wp == who_t) & (tp == when_t)).float().mean().item())

                if tracer_loss is not None and math.isfinite(float(tracer_loss)):
                    # step the same PPO optimizer so LM gets gradients; step tracer head optimizer for head params
                    ppo.optimizer.zero_grad(set_to_none=True)
                    tracer_optim.zero_grad(set_to_none=True)
                    ppo.accelerator.backward(args.lambda_tracer * tracer_loss)
                    ppo.optimizer.step()
                    tracer_optim.step()
                    tracer_loss_val = float(tracer_loss.detach().item())

            # -------- Counterfactual Replay (fast, optional) --------
            if args.cfr_prob > 0.0 and args.cfr_max_per_batch > 0:
                cf_queries, cf_resps, cf_scores = [], [], []
                added = 0
                for i, (pred_text, ga, gs) in enumerate(zip(conts, gold_agents, gold_steps)):
                    if added >= args.cfr_max_per_batch:
                        break
                    pp = _parse_first_pair(pred_text, allowed)
                    gold_ok = (ga is not None)
                    wrong = True
                    if pp is not None and gold_ok:
                        pa, ps = pp
                        wrong = not (pa.lower() == str(ga).lower() and int(ps) == int(gs))
                    # Only replay mistakes with some probability
                    if wrong and rng.random() < args.cfr_prob:
                        tgt = f" {str(ga).capitalize()} {int(gs)}"
                        resp_ids = tok.encode(tgt, add_special_tokens=False)
                        if resp_ids:
                            cf_resps.append(torch.tensor(resp_ids, device=device, dtype=torch.long))
                            cf_queries.append(input_ids[i])
                            cf_scores.append(torch.tensor(float(args.cfr_reward), device=device, dtype=torch.float32))
                            added += 1

                if cf_resps:
                    try:
                        ppo.step(cf_queries, cf_resps, cf_scores)
                    except Exception as e:
                        msg = str(e)
                        if "expected a non-empty list of Tensors" in msg or "empty internal batch" in msg:
                            print("[skip] CFR produced an empty internal batch; continuing.")
                        else:
                            raise
            # --------------------------------------------------------

            # ---------- logging ----------
            step_idx += 1
            log_row = {
                "step": step_idx,
                "reward_mean": float(sum(rewards) / max(1, len(rewards))),
            }
            if tracer is not None:
                if tracer_loss_val is not None: log_row["tracer_loss"] = tracer_loss_val
                if who_acc is not None:        log_row["who_acc"] = who_acc
                if when_acc is not None:       log_row["when_acc"] = when_acc
                if joint_acc is not None:      log_row["joint_acc"] = joint_acc
            logger.log(**log_row)

    os.makedirs(args.save_dir, exist_ok=True)
    ppo.model.save_pretrained(args.save_dir)
    tok.save_pretrained(args.save_dir)
    print(f"Saved PPO model to {args.save_dir}")

if __name__ == "__main__":
    main()

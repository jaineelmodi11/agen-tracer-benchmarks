#!/usr/bin/env python3
"""
Build a mixed attribution dataset from who_when.train.jsonl.

- Reads input rows with fields:
  { "query": str, "steps": [str, ...], "label": {"agent": str, "step": int} }
  (also tolerates top-level "agent"/"step" instead of label.*)

- Emits a JSONL with a mix of:
  * oracle copies (unchanged, n_oracle times per source row)
  * fault-injected copies (n_fault times per source row)

Fault injection (simple but effective):
  - randomly flip the agent to a different valid agent
  - or jitter the step index within [0, len(steps)-1]
  - keep the text trajectory the same (we’re supervising the *answer* fields)

This is enough to scale PPO training signal without changing your eval format.
"""

import os, sys, json, random, argparse
from typing import List, Dict, Any

VALID_AGENTS = ["coder", "analyst", "planner", "web", "coordinator"]

def load_jsonl(path: str) -> List[Dict[str, Any]]:
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            s = line.strip()
            if not s:
                continue
            try:
                r = json.loads(s)
            except Exception as e:
                raise SystemExit(f"[ERR] JSON parse error on line {i}: {e}")
            rows.append(r)
    return rows

def normalize_label(r: Dict[str, Any]) -> Dict[str, Any]:
    lbl = r.get("label") or {}
    agent = lbl.get("agent", r.get("agent", "")).strip().lower()
    step  = int(lbl.get("step",  r.get("step", 0)))
    return {"agent": agent, "step": step}

def pick_other_agent(agent: str) -> str:
    # choose a different valid agent
    choices = [a for a in VALID_AGENTS if a != agent]
    return random.choice(choices) if choices else agent

def clamp_step(step: int, n_steps: int) -> int:
    if n_steps <= 0:
        return 0
    return max(0, min(step, n_steps - 1))

def jitter_step(step: int, n_steps: int) -> int:
    if n_steps <= 1:
        return 0
    # small random shift; ensure it differs from original
    candidates = set(range(n_steps))
    candidates.discard(step)
    return random.choice(sorted(candidates))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", dest="out", required=True)
    ap.add_argument("--n-fault", type=int, default=2)
    ap.add_argument("--n-oracle", type=int, default=0)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    random.seed(args.seed)

    inp_abs  = os.path.abspath(args.inp)
    out_abs  = os.path.abspath(args.out)
    os.makedirs(os.path.dirname(out_abs), exist_ok=True)

    print(f"[build] input : {inp_abs}")
    print(f"[build] output: {out_abs}")
    print(f"[build] n_fault={args.n_fault} n_oracle={args.n_oracle} seed={args.seed}")

    if not os.path.exists(inp_abs):
        raise SystemExit(f"[ERR] input not found: {inp_abs}")

    src = load_jsonl(inp_abs)
    if not src:
        raise SystemExit(f"[ERR] no rows found in {inp_abs}")

    out = open(out_abs, "w", encoding="utf-8")
    n_emit = 0

    for r in src:
        q = r.get("query", "")
        steps = list(r.get("steps", []))
        lbl = normalize_label(r)
        agent = lbl["agent"]
        step  = clamp_step(lbl["step"], len(steps))

        # emit oracles
        for _ in range(args.n_oracle):
            ex = {
                "query": q,
                "steps": steps,
                "label": {"agent": agent, "step": step}
            }
            out.write(json.dumps(ex, ensure_ascii=False) + "\n")
            n_emit += 1

        # emit faults
        for _ in range(args.n_fault):
            if random.random() < 0.5:
                # flip agent
                new_agent = pick_other_agent(agent if agent in VALID_AGENTS else "coder")
                new_step  = step
            else:
                # jitter step
                new_agent = agent if agent in VALID_AGENTS else "coder"
                new_step  = jitter_step(step, len(steps))
            ex = {
                "query": q,
                "steps": steps,
                "label": {"agent": new_agent, "step": new_step}
            }
            out.write(json.dumps(ex, ensure_ascii=False) + "\n")
            n_emit += 1

    out.close()
    print(f"[build] wrote {n_emit} rows.")
    if not os.path.exists(out_abs) or os.path.getsize(out_abs) == 0:
        raise SystemExit("[ERR] output file missing or empty after write!")
    print("[build] done.")

if __name__ == "__main__":
    main()

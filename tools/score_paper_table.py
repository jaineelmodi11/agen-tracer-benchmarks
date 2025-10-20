#!/usr/bin/env python
# tools/score_paper_table.py
from __future__ import annotations
import argparse, json, os
from typing import Dict, Tuple, List

def score_file(path: str) -> Tuple[float, float, float, int]:
    """
    Returns: (agent_acc, step_acc, both_acc, n)
    """
    n = agent_ok = step_ok = both_ok = 0
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            r = json.loads(s)
            n += 1
            a_ok = (r.get("label_agent") is not None and r.get("who_pred") is not None and r.get("label_agent") == r.get("who_pred"))
            s_ok = (isinstance(r.get("label_step_idx0"), int) and isinstance(r.get("step_pred_idx0"), int)
                    and r.get("label_step_idx0") == r.get("step_pred_idx0"))
            agent_ok += int(bool(a_ok))
            step_ok  += int(bool(s_ok))
            both_ok  += int(bool(a_ok and s_ok))
    if n == 0:
        return 0.0, 0.0, 0.0, 0
    return agent_ok/n, step_ok/n, both_ok/n, n

def fmt(x: float) -> str:
    return f"{x*100:5.1f}%"

def main():
    ap = argparse.ArgumentParser(description="Paper-style compact table (Agent/Step ACC)")
    ap.add_argument("--base-withG", required=True)
    ap.add_argument("--base-withoutG", required=True)
    ap.add_argument("--sft-withG", required=True)
    ap.add_argument("--sft-withoutG", required=True)
    ap.add_argument("--extra", default="",
                    help='Optional comma-separated extras like: "RL withG=checkpoints/ppo.withG.jsonl,RL w/oG=checkpoints/ppo.withoutG.jsonl"')
    args = ap.parse_args()

    cols: List[Tuple[str, str]] = [
        ("Base w/G", args.base_withG),
        ("Base w/oG", args.base_withoutG),
        ("SFT w/G", args.sft_withG),
        ("SFT w/oG", args.sft_withoutG),
    ]
    if args.extra.strip():
        for chunk in args.extra.split(","):
            if not chunk.strip():
                continue
            if "=" not in chunk:
                raise SystemExit(f"--extra entry must be Name=path : {chunk!r}")
            name, path = chunk.split("=", 1)
            cols.append((name.strip(), path.strip()))

    results: Dict[str, Tuple[float,float,float,int]] = {}
    for name, path in cols:
        if not os.path.exists(path):
            raise SystemExit(f"Missing file for {name}: {path}")
        results[name] = score_file(path)

    # Render table
    names = [c[0] for c in cols]
    print("\nPaper-style summary (ACC):\n")
    header = "Metric        " + "  ".join(f"{n:>14}" for n in names)
    print(header)
    print("-"*len(header))
    rowA = "Agent Acc     " + "  ".join(f"{fmt(results[n][0]):>14}" for n in names)
    rowS = "Step Acc      " + "  ".join(f"{fmt(results[n][1]):>14}" for n in names)
    rowB = "Both Acc      " + "  ".join(f"{fmt(results[n][2]):>14}" for n in names)
    rowN = "N (samples)   " + "  ".join(f"{results[n][3]:>14d}" for n in names)
    print(rowA)
    print(rowS)
    print(rowB)
    print(rowN)
    print()

if __name__ == "__main__":
    main()

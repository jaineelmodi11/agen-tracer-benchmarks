#!/usr/bin/env python
from __future__ import annotations
import argparse, json, os, sys

# path setup so running from repo root works
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(TOOLS_DIR)
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# prefer package import, fallback to src.*
try:
    from atracer.faults import FaultInjector
    from atracer.utils_agents import canonicalize_agent
except ModuleNotFoundError:
    from src.atracer.faults import FaultInjector  # type: ignore
    from src.atracer.utils_agents import canonicalize_agent  # type: ignore


def load_jsonl(path: str):
    with open(path, "r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            s = line.strip()
            if not s:
                continue
            try:
                yield json.loads(s)
            except Exception as e:
                print(f"[inject_faults] bad JSON in {path}:{lineno}: {e}", file=sys.stderr)
                continue

def save_jsonl(rows, path: str):
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def main():
    ap = argparse.ArgumentParser(
        description="Fault injection: synthesize failing trajectories from successful ones, labeling (agent, step)."
    )
    ap.add_argument("--in", dest="inp", required=True, help="input JSONL (ideally successes)")
    ap.add_argument("--out", required=True, help="output JSONL of synthesized FAILURES with labels")
    ap.add_argument("--k", type=int, default=3, help="max steps to sample per trajectory for injection")
    ap.add_argument("--assume-success", action="store_true",
                    help="attempt injection on ALL rows (ignore is_success flag)")
    args = ap.parse_args()

    inj = FaultInjector()

    processed = 0
    attempted = 0
    synthesized = 0
    out_rows = []

    for traj in load_jsonl(args.inp):
        processed += 1
        is_success = bool(traj.get("is_success"))
        if not is_success and not args.assume_success:
            # only transform explicit successes unless forced
            out_rows.append(traj)
            continue

        attempted += 1
        new_traj, label = inj.inject_once(traj, k_sample=args.k)
        if label:
            # canonicalize label and attach
            label["agent"] = canonicalize_agent(label.get("agent")) or "unknown"
            new_traj["label"] = label
            out_rows.append(new_traj)
            synthesized += 1
        else:
            # could not inject; keep original trajectory
            out_rows.append(traj)

    print(
        f"[inject_faults] processed={processed} | attempted={attempted} | synthesized={synthesized}",
        file=sys.stderr,
    )
    save_jsonl(out_rows, args.out)

if __name__ == "__main__":
    main()

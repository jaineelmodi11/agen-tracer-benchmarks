#!/usr/bin/env python
from __future__ import annotations
import argparse, json, sys, os

# ----- Make sibling 'src/' importable when running this tool -----
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(TOOLS_DIR)          # go UP from tools/
SRC_DIR = os.path.join(PROJECT_ROOT, "src")        # <repo-root>/src
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# Try to import as a proper package ('atracer') first, then fallback.
try:
    from atracer.cf_replay import earliest_decisive_error
    from atracer.cf_oracles import HeuristicOracle, MockJudge
    from atracer.utils_agents import canonicalize_agent
except ModuleNotFoundError:
    from src.atracer.cf_replay import earliest_decisive_error  # type: ignore
    from src.atracer.cf_oracles import HeuristicOracle, MockJudge  # type: ignore
    from src.atracer.utils_agents import canonicalize_agent  # type: ignore


def load_jsonl(path: str, *, loose: bool = False):
    """
    Yield JSON objects from a JSONL file.
    - Skips fully blank lines.
    - If loose=True: skips malformed lines with a warning instead of raising.
    """
    with open(path, "r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            s = line.strip()
            if not s:
                continue
            try:
                yield json.loads(s)
            except json.JSONDecodeError as e:
                snippet = s[:120].replace("\t", "\\t")
                msg = (
                    f"[cf_label_failed] JSON parse error in {path}:{lineno}: {e.msg} "
                    f"(pos {e.pos}) | snippet: {snippet!r}"
                )
                if loose:
                    print(msg + "  -- skipping line due to --loose", file=sys.stderr)
                    continue
                else:
                    print(msg, file=sys.stderr)
                    raise

def save_jsonl(rows, path: str):
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def main():
    ap = argparse.ArgumentParser(
        description="Counterfactual replay labeling for FAILED trajectories: find earliest decisive (agent, step)."
    )
    ap.add_argument("--in", dest="inp", required=True, help="input JSONL of trajectories (ideally failures)")
    ap.add_argument("--out", required=True, help="output JSONL with label.agent / label.step added when found")
    ap.add_argument("--dry-run", action="store_true", help="print summary only; do not write output file")
    ap.add_argument("--loose", action="store_true", help="skip malformed JSONL lines instead of failing")
    ap.add_argument("--require-fail", action="store_true", default=True,
                    help="only attempt CF on rows with is_success == False (default: on)")
    args = ap.parse_args()

    oracle = HeuristicOracle()
    judge = MockJudge()

    processed = 0
    skipped_success = 0
    attempted = 0
    labeled = 0
    out_rows = []

    for traj in load_jsonl(args.inp, loose=args.loose):
        processed += 1
        # Skip already-successful rows if requested
        if args.require_fail and bool(traj.get("is_success")):
            skipped_success += 1
            out_rows.append(traj)
            continue

        attempted += 1
        res = earliest_decisive_error(traj, oracle, judge)
        if res.found and res.step is not None:
            labeled += 1
            lab = traj.get("label") or {}
            lab["agent"] = canonicalize_agent(res.agent) or "unknown"
            lab["step"] = int(res.step)
            traj["label"] = lab
            meta = traj.setdefault("__cf_meta__", {})
            meta["source"] = "counterfactual_replay"
        out_rows.append(traj)

    print(
        f"[cf_label_failed] processed={processed} | skipped_success={skipped_success} "
        f"| attempted={attempted} | labeled={labeled}",
        file=sys.stderr,
    )

    if not args.dry_run:
        save_jsonl(out_rows, args.out)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import argparse, json, re, sys
from collections import Counter

ERR_PAT = re.compile(
    r"(error|exception|traceback|typeerror|keyerror|zerodivision|valueerror|indexerror|not found|undefined|fail(ed)?)",
    re.IGNORECASE,
)

def find_fail_idx0(steps):
    """
    Heuristic: pick the first step with a clear failure signal.
    - prefer `error` field if present & truthy
    - else look for error-y text in `obs` or `action`
    - fallback: last step (if any), else None
    """
    if not isinstance(steps, list) or not steps:
        return None
    for i, s in enumerate(steps):
        if isinstance(s, dict):
            if s.get("error"):
                return i
            for k in ("obs", "action"):
                v = s.get(k)
                if isinstance(v, str) and ERR_PAT.search(v):
                    return i
    return len(steps) - 1

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="input JSONL")
    ap.add_argument("--out", required=True, help="output JSONL with relabeled steps")
    ap.add_argument("--keep_agent", action="store_true",
                    help="keep existing label.agent unchanged if present")
    args = ap.parse_args()

    n = 0
    dist = Counter()
    bad = 0

    with open(args.src, "r", encoding="utf-8") as fin, open(args.out, "w", encoding="utf-8") as fout:
        for line in fin:
            if not line.strip():
                continue
            rec = json.loads(line)
            steps = rec.get("steps") or rec.get("actions") or []
            idx0 = find_fail_idx0(steps)
            if idx0 is None:
                bad += 1
                fout.write(json.dumps(rec, ensure_ascii=False) + "\n")
                continue

            lab = rec.get("label") or {}
            # keep/repair label.agent
            agent = lab.get("agent")
            # If anonymized AgentA/AgentB/etc., keep as-is; scoring can map them to 'unknown' in without-G
            # If you want canonical agents and there's a clear agent at idx0, you could do:
            #   a = steps[idx0].get("agent"); if a in {'coder','analyst','planner','web','coordinator'}: agent = a
            lab["agent"] = agent
            # write new step (0-based here); your eval expects 0-based
            lab["step"] = int(idx0)
            rec["label"] = lab

            dist[idx0] += 1
            n += 1
            fout.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"Wrote {n} examples to {args.out} (skipped={bad})")
    if dist:
        print("New step distribution (0-based):", dict(sorted(dist.items())))

if __name__ == "__main__":
    main()

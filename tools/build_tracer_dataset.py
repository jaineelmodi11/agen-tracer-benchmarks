#!/usr/bin/env python
from __future__ import annotations
import argparse, json, os, sys

def load_jsonl(path: str):
    with open(path, "r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            s = line.strip()
            if not s:
                continue
            try:
                yield json.loads(s)
            except Exception as e:
                print(f"[build_tracer_dataset] bad JSON in {path}:{lineno}: {e}", file=sys.stderr)

def save_jsonl(rows, path: str):
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def main():
    ap = argparse.ArgumentParser(
        description="Merge CF-labeled failures (D-) and injected failures (D+) into a single training set."
    )
    ap.add_argument("--cf-fail", required=True, help="JSONL of failures labeled by counterfactual replay")
    ap.add_argument("--inj-fail", required=True, help="JSONL of synthesized failures via fault injection")
    ap.add_argument("--out", required=True, help="Output JSONL for training (D_tracer)")
    ap.add_argument("--require-label", action="store_true", default=True,
                    help="Only include rows that carry `label.agent` and `label.step` (default: on)")
    args = ap.parse_args()

    total = kept = 0
    merged = []

    def valid_lab(row):
        lab = row.get("label") or {}
        return isinstance(lab.get("step"), int) and isinstance(lab.get("agent"), str) and lab["agent"].strip()

    for src in (args.cf_fail, args.inj_fail):
        for r in load_jsonl(src):
            total += 1
            if args.require_label and not valid_lab(r):
                continue
            kept += 1
            merged.append(r)

    print(f"[build_tracer_dataset] loaded={total} | kept={kept} | out={args.out}", file=sys.stderr)
    save_jsonl(merged, args.out)

if __name__ == "__main__":
    main()

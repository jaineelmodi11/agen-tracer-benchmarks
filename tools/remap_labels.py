#!/usr/bin/env python
from __future__ import annotations
import argparse, json, os, sys
from typing import Dict, Any

def parse_map(map_str: str) -> Dict[str, str]:
    """
    Parse a mapping like:
      "agenta:coder,agentb:analyst,agentc:planner,agentd:web,agente:coordinator"
    Returns a lowercase dict {src: dst}.
    """
    m: Dict[str, str] = {}
    if not map_str:
        return m
    for pair in map_str.split(","):
        pair = pair.strip()
        if not pair or ":" not in pair:
            continue
        src, dst = pair.split(":", 1)
        src = src.strip().lower()
        dst = dst.strip().lower()
        if src and dst:
            m[src] = dst
    return m

def load_jsonl(path: str):
    with open(path, "r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            s = line.strip()
            if not s:
                continue
            try:
                yield json.loads(s)
            except Exception as e:
                print(f"[remap_labels] bad JSON in {path}:{lineno}: {e}", file=sys.stderr)

def save_jsonl(rows, path: str):
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def remap_agent_string(s: str | None, mapping: Dict[str, str]) -> str | None:
    if s is None:
        return None
    k = str(s).strip().lower()
    return mapping.get(k, k) if k else None

def remap_row(row: Dict[str, Any], mapping: Dict[str, str], steps_too: bool) -> Dict[str, Any]:
    # Remap label.agent if present
    lab = row.get("label")
    if isinstance(lab, dict) and "agent" in lab:
        lab["agent"] = remap_agent_string(lab.get("agent"), mapping)
        row["label"] = lab

    if steps_too:
        steps = row.get("steps")
        if isinstance(steps, list):
            new_steps = []
            for s in steps:
                if isinstance(s, dict):
                    if "agent" in s:
                        s["agent"] = remap_agent_string(s.get("agent"), mapping)
                    if "role" in s:
                        s["role"] = remap_agent_string(s.get("role"), mapping)
                new_steps.append(s)
            row["steps"] = new_steps
    return row

def main():
    ap = argparse.ArgumentParser(description="Remap masked agent labels to canonical roles.")
    ap.add_argument("--in", dest="inp", required=True, help="input JSONL")
    ap.add_argument("--out", required=True, help="output JSONL")
    ap.add_argument(
        "--map",
        required=True,
        help="mapping like 'agenta:coder,agentb:analyst,agentc:planner,agentd:web,agente:coordinator'",
    )
    ap.add_argument("--steps-too", action="store_true", help="also remap 'agent'/ 'role' fields in steps[]")
    args = ap.parse_args()

    mapping = parse_map(args.map)
    if not mapping:
        print("[remap_labels] WARNING: empty mapping provided; output will be identical.", file=sys.stderr)

    total = 0
    changed = 0
    out_rows = []

    for row in load_jsonl(args.inp):
        total += 1
        before = json.dumps(row, ensure_ascii=False)
        row = remap_row(row, mapping, steps_too=args.steps_too)
        after = json.dumps(row, ensure_ascii=False)
        if after != before:
            changed += 1
        out_rows.append(row)

    print(f"[remap_labels] processed={total} | changed={changed}", file=sys.stderr)
    save_jsonl(out_rows, args.out)

if __name__ == "__main__":
    main()

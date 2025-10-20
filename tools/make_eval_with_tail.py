#!/usr/bin/env python3
import argparse, json, sys, re

TAIL = (
    "\n\n---\n"
    "At the VERY END, output ONLY ONE line in the exact format:\n"
    "<agent> <step>\n"
    "where <agent> is one of {coder, analyst, planner, coordinator, web}\n"
    "and <step> is an integer in {0,1,2,3,4}. Do NOT add any extra words after that line."
)

def main():
    ap = argparse.ArgumentParser(description="Append strict tail instruction to eval JSONL.")
    ap.add_argument("--in",  dest="inp", required=True, help="input eval JSONL")
    ap.add_argument("--out", dest="out", required=True, help="output JSONL with tail instruction appended")
    ap.add_argument("--field", default="", help="force which field to append to (query|prompt|input); default: auto")
    args = ap.parse_args()

    n=0
    with open(args.inp, "r", encoding="utf-8") as fin, open(args.out, "w", encoding="utf-8") as fout:
        for line in fin:
            if not line.strip(): 
                continue
            row = json.loads(line)
            field = args.field or ("query" if "query" in row else "prompt" if "prompt" in row else "input" if "input" in row else None)
            if not field:
                print(f"[make_eval_with_tail] WARN: no query/prompt/input field; writing unchanged", file=sys.stderr)
            else:
                row[field] = (row.get(field) or "") + TAIL
            fout.write(json.dumps(row, ensure_ascii=False) + "\n")
            n += 1
    print(f"[make_eval_with_tail] wrote {n} rows to {args.out}", file=sys.stderr)

if __name__ == "__main__":
    main()

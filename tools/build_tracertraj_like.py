#!/usr/bin/env python
import json, random, argparse
random.seed(13)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="src", required=True)
    ap.add_argument("--out-train", required=True)
    ap.add_argument("--out-val", required=True)
    ap.add_argument("--val-ratio", type=float, default=0.1)
    args = ap.parse_args()

    rows = [json.loads(l) for l in open(args.src)]
    random.shuffle(rows)
    n = len(rows)
    nv = max(1, int(n * args.val_ratio))
    val = rows[:nv]
    train = rows[nv:]

    def pack(r):
        return {
            "query": r.get("query",""),
            "steps": r.get("steps", []),
            "label": {
                "agent": r["label"]["agent"],
                "step": int(r["label"]["step"])
            }
        }

    with open(args.out_train, "w") as f:
        for r in train: f.write(json.dumps(pack(r)) + "\n")
    with open(args.out_val, "w") as f:
        for r in val:   f.write(json.dumps(pack(r)) + "\n")

if __name__ == "__main__":
    main()

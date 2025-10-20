"""
Map your raw Who&When-style JSON into our jsonl schema (train/val).
Adjust field names to your raw file.
"""
import argparse, json, random
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out-prefix", required=True)
    ap.add_argument("--val-ratio", type=float, default=0.2)
    args = ap.parse_args()

    with open(args.inp, "r", encoding="utf-8") as f:
        raw = json.load(f)

    rows = []
    for ex in raw:
        steps = []
        for t, st in enumerate(ex.get("trajectory", [])):
            steps.append({
                "t": t,
                "agent": st.get("agent", "Agent"),
                "action": st.get("action", ""),
                "obs": st.get("obs", ""),
                "error": st.get("error", None)
            })
        rows.append({
            "id": ex.get("id", f"ex_{len(rows)}"),
            "query": ex.get("query", ""),
            "steps": steps,
            "final_status": ex.get("final_status", "fail"),
            "label": {"agent": ex["label"]["agent"], "step": int(ex["label"]["step"])},
        })

    random.shuffle(rows)
    n_val = int(len(rows) * args.val_ratio)
    val = rows[:n_val]; train = rows[n_val:]

    out_tr = Path(args.out_prefix + ".train.jsonl")
    out_va = Path(args.out_prefix + ".val.jsonl")
    with out_tr.open("w", encoding="utf-8") as f:
        for r in train:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with out_va.open("w", encoding="utf-8") as f:
        for r in val:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main()

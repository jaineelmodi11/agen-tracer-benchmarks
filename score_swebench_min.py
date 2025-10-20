from __future__ import annotations
import argparse, json, os, re
from typing import Dict, List, Any, Tuple

def load_jsonl(path: str) -> List[Dict[str, Any]]:
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if ln:
                rows.append(json.loads(ln))
    return rows

def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gold", required=True, help="Gold JSONL (lite format)")
    ap.add_argument("--pred", required=True, help="Predictions JSONL from eval_swebench_min.py")
    ap.add_argument("--out", required=True, help="Path to write JSON metrics")
    args = ap.parse_args()

    gold = load_jsonl(args.gold)
    pred = load_jsonl(args.pred)
    gold_by_id = {}
    for g in gold:
        iid = g.get("instance_id") or g.get("id") or g.get("slug")
        if iid is None:
            continue
        gold_by_id[str(iid)] = g

    exact = kw = overall = 0
    total = 0
    per: List[Dict[str, Any]] = []

    for p in pred:
        iid = str(p.get("instance_id"))
        if iid not in gold_by_id:
            continue
        total += 1
        g = gold_by_id[iid]
        comp = norm(p.get("completion", ""))

        exact_ok = False
        gold_text = g.get("gold")
        if isinstance(gold_text, str) and gold_text.strip():
            exact_ok = norm(gold_text) in comp

        kw_ok = False
        kws = g.get("gold_keywords")
        if isinstance(kws, list) and kws:
            kw_ok = all(norm(k) in comp for k in kws if isinstance(k, str) and k.strip())

        ex_ok = 1 if exact_ok else 0
        kw_ok_i = 1 if kw_ok else 0
        best = 1 if (exact_ok or kw_ok) else 0

        exact += ex_ok
        kw += kw_ok_i
        overall += best

        per.append({"instance_id": iid, "exact": bool(exact_ok), "keywords": bool(kw_ok), "correct": bool(best)})

    metrics = {
        "num_examples": total,
        "exact_acc": (exact / total) if total else 0.0,
        "keyword_acc": (kw / total) if total else 0.0,
        "overall_acc": (overall / total) if total else 0.0,
        "per_example": per[:200],  # truncate preview
    }
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    print(json.dumps(metrics, indent=2))

if __name__ == "__main__":
    main()

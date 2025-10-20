#!/usr/bin/env python
import json, argparse

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gold", required=True)  # gold jsonl with fields: instance_id, oracle_passed (bool)
    ap.add_argument("--pred", required=True)  # pred jsonl with fields: instance_id, passed (bool) OR prediction to compare
    ap.add_argument("--out",  required=True)
    args = ap.parse_args()

    gold = {}
    with open(args.gold) as f:
        for ln in f:
            d = json.loads(ln)
            gold[d["instance_id"]] = d

    ok = tot = 0
    with open(args.pred) as f:
        for ln in f:
            p = json.loads(ln)
            iid = p["instance_id"]
            if iid not in gold: continue
            # If your evaluator writes p["passed"]=True/False, use that
            if "passed" in p:
                hit = bool(p["passed"])
            else:
                # fallback: exact match against a target patch string in gold (rarely used)
                hit = (p.get("prediction","") == gold[iid].get("target",""))
            ok += int(hit); tot += 1

    out = {"overall_acc": (ok / tot if tot else 0.0), "ok": ok, "total": tot}
    with open(args.out, "w") as f: json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()

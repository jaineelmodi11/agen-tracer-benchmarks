import json, sys
if len(sys.argv) < 3:
    print("usage: python scripts/eval_who_when.py <pred.jsonl> <gold.jsonl>")
    sys.exit(1)

def read_jsonl(p):
    with open(p) as f:
        for line in f:
            line=line.strip()
            if line:
                yield json.loads(line)

pred = {j["id"]: j for j in read_jsonl(sys.argv[1])}
gold = {j["id"]: j for j in read_jsonl(sys.argv[2])}

ok=0; total=0; missing=[]
for k,g in gold.items():
    if k not in pred:
        missing.append(k)
        continue
    total += 1
    ok += int(pred[k].get("answer") == g.get("answer"))

acc = (100*ok/max(total,1))
out = {"correct": ok, "total": total, "acc": round(acc,2), "missing": missing}
print(json.dumps(out, indent=2))

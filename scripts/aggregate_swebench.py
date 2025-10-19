import json, sys, glob
paths = sys.argv[1:] or sorted(glob.glob("swebench/runs/*.json"))
resolved = submitted = 0
per_run = []
for p in paths:
    with open(p) as f:
        j = json.load(f)
    r = j.get("resolved_instances", 0)
    s = j.get("submitted_instances", 0)
    per_run.append({"file": p, "resolved": r, "submitted": s})
    resolved += r; submitted += s

pct = (100.0 * resolved / submitted) if submitted else 0.0
print(json.dumps({"resolved": resolved, "submitted": submitted, "pct": round(pct,2), "runs": per_run}, indent=2))

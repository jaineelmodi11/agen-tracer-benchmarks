import json, sys, os
"""
Converts your predictions into EvalPlus samples.jsonl

Accepted input schema (per line, JSON):
- "task_id" or "id" (e.g., "HumanEval/0")
- Either:
    * "solution": full function with signature, or
    * "completion": body only (EvalPlus accepts this too)
- Optionally:
    * "solutions": list[str]  (if you have multiple candidates per task)
    * "completions": list[str]
Writes to coding/humaneval/samples.jsonl
"""
if len(sys.argv)<2:
    print("usage: python scripts/convert_to_evalplus.py <input_predictions.jsonl>")
    sys.exit(1)

inp = sys.argv[1]
outp = "coding/humaneval/samples.jsonl"
os.makedirs(os.path.dirname(outp), exist_ok=True)
n=0
with open(outp, "w") as out:
    for line in open(inp):
        line=line.strip()
        if not line: continue
        obj = json.loads(line)
        tid = obj.get("task_id") or obj.get("id")
        if not tid: continue

        wrote = False
        if "solutions" in obj and isinstance(obj["solutions"], list):
            for sol in obj["solutions"]:
                out.write(json.dumps({"task_id": tid, "solution": sol})+"\n")
                n+=1; wrote=True
        if "completions" in obj and isinstance(obj["completions"], list):
            for comp in obj["completions"]:
                out.write(json.dumps({"task_id": tid, "completion": comp})+"\n")
                n+=1; wrote=True
        if not wrote:
            sol = obj.get("solution")
            comp = obj.get("completion")
            if sol:
                out.write(json.dumps({"task_id": tid, "solution": sol})+"\n"); n+=1
            elif comp:
                out.write(json.dumps({"task_id": tid, "completion": comp})+"\n"); n+=1

print(f"wrote {n} samples to {outp}")

import json, sys

def read_ids(path):
    s=set()
    for line in open(path):
        line=line.strip()
        if not line: continue
        try:
            obj=json.loads(line)
            iid = obj.get("instance_id") or obj.get("id")
            if iid: s.add(iid)
        except: pass
    return s

if len(sys.argv)<3:
    print("usage: python scripts/compare_jsonl_ids.py <fileA.jsonl> <fileB.jsonl>")
    sys.exit(1)

a,b = read_ids(sys.argv[1]), read_ids(sys.argv[2])
print(json.dumps({
  "A_only": sorted(a-b),
  "B_only": sorted(b-a),
  "both_count": len(a & b)
}, indent=2))

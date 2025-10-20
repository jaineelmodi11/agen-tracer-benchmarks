# tools/harden_withoutG.py
import re, json, sys, random

def scrub_text(s: str) -> str:
    if not isinstance(s, str): return s
    # Hide “Step 2”, “Action 3”, “at step 2”, “step-2”, etc.
    s = re.sub(r'\b(Step|Action)\s*\d+\b', r'\1 X', s, flags=re.IGNORECASE)
    s = re.sub(r'\bat\s+(step|action)\s*\d+\b', r'at \1 X', s, flags=re.IGNORECASE)
    s = re.sub(r'\b(step|action)\s*[-:]?\s*\d+\b', r'\1 X', s, flags=re.IGNORECASE)
    # Also hide bare “#2”, “(2)”, “ t=2 ” style indices when they look like step refs
    s = re.sub(r'(?<!\w)(?:#|\()?\s*\d+\s*(?:\))?(?!\w)', lambda m: m.group(0).replace(m.group(0), ' X '), s)
    # Keep error names (TypeError, 404) to preserve some agent signal
    return re.sub(r'\s+', ' ', s).strip()

def harden(rec):
    # Scrub query
    if 'query' in rec: rec['query'] = scrub_text(rec['query'])
    # Scrub steps' textual fields, not the labels
    steps = rec.get('steps')
    if isinstance(steps, list):
        for st in steps:
            for k in ('action','obs','note','msg','text'):
                if k in st: st[k] = scrub_text(st[k])
    return rec

def main(src, dst):
    n = 0
    with open(src, 'r', encoding='utf-8') as f, open(dst, 'w', encoding='utf-8') as w:
        for line in f:
            rec = harden(json.loads(line))
            w.write(json.dumps(rec, ensure_ascii=False) + '\n')
            n += 1
    print(f"Hardened {n} examples -> {dst}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: python tools/harden_withoutG.py <in.jsonl> <out.jsonl>")
        sys.exit(2)
    main(sys.argv[1], sys.argv[2])

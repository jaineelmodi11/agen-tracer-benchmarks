# tools/score_preds_robust.py
#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, collections, sys

PAIR_RE = re.compile(r"\b(analyst|coder|planner|web|coordinator)\b\D{0,80}(\d{1,3})", re.I)

_ALIASES = {"coordinator": "planner"}

def _canon(a: str | None) -> str:
    a = (a or "").strip().lower()
    return _ALIASES.get(a, a)

def _read_preds(path):
    preds = []
    bad = 0
    with open(path, "r", encoding="utf-8") as f:
        for ln in f:
            s = ln.strip()
            if not s:
                preds.append((None, None)); continue
            m = PAIR_RE.search(s)
            if m:
                agent = _canon(m.group(1))
                step = int(m.group(2))
                preds.append((agent, step))
            else:
                parts = s.split()
                if len(parts) >= 2 and parts[1].isdigit():
                    preds.append((_canon(parts[0]), int(parts[1])))
                else:
                    preds.append((None, None)); bad += 1
    if bad:
        print(f"[warn] {bad} lines in preds had no (agent,step) pair; counted as incorrect.", file=sys.stderr)
    return preds

def _read_gold(path):
    gold = []
    with open(path, "r", encoding="utf-8") as f:
        for ln in f:
            if not ln.strip(): continue
            r = json.loads(ln)
            lab = r.get("label") or {}
            agent = _canon((lab.get("agent") or r.get("agent") or ""))
            step = int(lab.get("step") or r.get("step") or 0)
            gold.append((agent, step))
    return gold

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preds", required=True)
    ap.add_argument("--gold", required=True)
    ap.add_argument("--gold-remapped", action="store_true")  # kept for CLI compatibility; no-op
    args = ap.parse_args()

    P = _read_preds(args.preds)
    G = _read_gold(args.gold)

    if len(P) != len(G):
        print(f"length mismatch: gold={len(G)} pred={len(P)}", file=sys.stderr)
        n = min(len(P), len(G)); P, G = P[:n], G[:n]

    n = len(P)
    def eq(a,b): return (a is not None) and (b is not None) and (a==b)

    agent_acc = sum(eq(pa,ga) for (pa,_),(ga,_) in zip(P,G)) / n
    step_acc  = sum((ps is not None) and (ps==gs) for (_,ps),(_,gs) in zip(P,G)) / n
    both_acc  = sum(eq(pa,ga) and (ps is not None) and (ps==gs) for (pa,ps),(ga,gs) in zip(P,G)) / n

    print({"samples": n, "agent_acc": agent_acc, "step_acc": step_acc, "both_acc": both_acc})
    print({"samples": n, "agent_acc": agent_acc, "step_acc": step_acc, "both_acc": both_acc})

    by = collections.defaultdict(list)
    for (pa,ps),(ga,gs) in zip(P,G):
        by[ga].append( (eq(pa,ga), (ps is not None) and (ps==gs), eq(pa,ga) and (ps is not None) and (ps==gs)) )

    print("per-agent:")
    for ga, lst in by.items():
        m = len(lst)
        a = sum(x[0] for x in lst)/m
        s = sum(x[1] for x in lst)/m
        b = sum(x[2] for x in lst)/m
        print(ga.title(), {"n": m, "agent_acc": a, "step_acc": s, "both_acc": b})

if __name__ == "__main__":
    main()

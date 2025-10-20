# tools/build_tracertraj.py
import argparse, json, random, re, pathlib
from typing import Dict, Any, List, Optional, Tuple

ERR_PAT = re.compile(r"(error|exception|traceback|failed|not found|keyerror|typeerror)", re.I)

def _load_jsonl(path: str) -> List[Dict[str, Any]]:
    out = []
    with open(path, encoding="utf-8") as f:
        for ln in f:
            if ln.strip():
                out.append(json.loads(ln))
    return out

def _find_first_error_step(steps: List[Dict[str, Any]]) -> Optional[Tuple[str, int]]:
    # Heuristic: earliest step whose "error" is truthy, else whose "obs" contains error words.
    for st in steps or []:
        a = (st.get("agent") or "").strip()
        t = st.get("t")
        if t is None: continue
        if st.get("error"):
            return (a, int(t))
        if ERR_PAT.search((st.get("obs") or "")):
            return (a, int(t))
    return None

def _normalize_agent_case(a: str) -> str:
    a = (a or "").strip()
    return a[:1].upper() + a[1:].lower() if a else a

def _ensure_label(rec: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    # If label exists and is valid, use it. Else, try to derive.
    lab = rec.get("label") or {}
    ga, gs = lab.get("agent"), lab.get("step")
    if isinstance(ga, str) and isinstance(gs, int) and gs >= 1:
        return {"agent": _normalize_agent_case(ga), "step": gs}

    # derive
    steps = rec.get("steps") or rec.get("trace") or []
    pair = _find_first_error_step(steps)
    if pair:
        a, s = pair
        if a:
            return {"agent": _normalize_agent_case(a), "step": max(1, int(s))}

    # final fallback: if we see any coder action at all, pick it; else analyst 1
    seen_coder = any((isinstance(st, dict) and (st.get("agent") or "").strip().lower() == "coder") for st in steps)
    return {"agent": "Coder" if seen_coder else "Analyst", "step": 1}

def _extract(rec: Dict[str, Any]) -> Tuple[str, List[Dict[str, Any]]]:
    q = rec.get("query") or rec.get("instruction") or rec.get("prompt") or rec.get("input") or ""
    steps = rec.get("steps") or rec.get("trace") or rec.get("rationale") or []
    return str(q), list(steps)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--withG", default="", help="JSONL with gold labels (optional)")
    ap.add_argument("--withoutG", default="", help="JSONL without labels (optional)")
    ap.add_argument("--outdir", default="data/tracertraj")
    ap.add_argument("--val_frac", type=float, default=0.05)
    ap.add_argument("--test_frac", type=float, default=0.05)
    args = ap.parse_args()

    rows: List[Dict[str, Any]] = []
    if args.withG:
        rows += _load_jsonl(args.withG)
    if args.withoutG:
        rows += _load_jsonl(args.withoutG)

    cleaned = []
    for r in rows:
        q, steps = _extract(r)
        lab = _ensure_label(r)
        if not q or not lab:
            continue
        cleaned.append({"id": r.get("id"), "query": q, "steps": steps, "label": lab})

    random.shuffle(cleaned)
    n = len(cleaned)
    n_test = int(n * args.test_frac)
    n_val = int(n * args.val_frac)

    test = cleaned[:n_test]
    val = cleaned[n_test:n_test+n_val]
    train = cleaned[n_test+n_val:]

    outdir = pathlib.Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    for name, data in [("train", train), ("val", val), ("test", test)]:
        p = outdir / f"{name}.jsonl"
        with open(p, "w", encoding="utf-8") as o:
            for rec in data:
                o.write(json.dumps(rec) + "\n")
        print(f"Wrote {p}  ({len(data)} rows)")

if __name__ == "__main__":
    main()


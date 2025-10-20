import argparse, json, os, glob, sys
from pathlib import Path

def iter_records_from_path(p: Path):
    for fp in sorted(glob.glob(str(p / "**" / "*"), recursive=True)):
        f = Path(fp)
        if not f.is_file(): 
            continue
        if f.suffix.lower() == ".jsonl":
            with f.open("r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        yield json.loads(line)
                    except Exception as e:
                        print(f"[warn] bad jsonl line in {f}: {e}", file=sys.stderr)
        elif f.suffix.lower() == ".json":
            try:
                obj = json.loads(f.read_text(encoding="utf-8"))
            except Exception as e:
                print(f"[warn] bad json in {f}: {e}", file=sys.stderr); 
                continue
            if isinstance(obj, list):
                for rec in obj:
                    yield rec
            elif isinstance(obj, dict):
                yield obj

def get_first(d: dict, *keys, default=None):
    for k in keys:
        if k in d and d[k] is not None:
            return d[k]
    return default

def coerce_int(x):
    try:
        return int(x)
    except Exception:
        try:
            # sometimes "step 3" → 3
            import re
            m = re.search(r"-?\d+", str(x))
            return int(m.group(0)) if m else None
        except Exception:
            return None

def normalize_steps(traj):
    steps = []
    if isinstance(traj, list):
        for t, st in enumerate(traj):
            if isinstance(st, dict):
                agent = get_first(st, "agent", "role", "name", default="Agent")
                action = get_first(st, "action", "content", "tool_input", "msg", default="")
                obs    = get_first(st, "obs", "observation", "tool_output", "output", default="")
                err    = get_first(st, "error", "err", default=None)
            else:
                agent, action, obs, err = "Agent", str(st), "", None
            steps.append({"t": t, "agent": agent, "action": action, "obs": obs, "error": err})
    return steps

def extract_label(ex: dict):
    """
    Try common label layouts in Who&When-style data:
      - top-level: who / when
      - top-level: responsible_agent / decisive_step
      - label: {agent, step}  OR  label: {who, when}
      - answer / annotation: {who, when}  OR {agent, step}
    """
    # direct
    who = get_first(ex, "who", "responsible_agent", "agent", default=None)
    when = get_first(ex, "when", "decisive_step", "step", "time_step", default=None)

    # nested under common containers
    for key in ("label", "answer", "annotation", "gold", "gt", "who_when"):
        sub = ex.get(key)
        if isinstance(sub, dict):
            who = who if who is not None else get_first(sub, "who", "responsible_agent", "agent")
            when = when if when is not None else get_first(sub, "when", "decisive_step", "step", "time_step")

    if who is None or when is None:
        return None

    when_i = coerce_int(when)
    if when_i is None:
        return None
    return {"agent": str(who), "step": when_i}

def map_to_ours(ex: dict, fallback_prefix: str):
    query = get_first(ex, "query", "instruction", "task", default="")
    traj  = get_first(ex, "trajectory", "steps", "logs", default=[])
    steps = normalize_steps(traj)
    rid   = get_first(ex, "id", "uid", default=f"{fallback_prefix}_{id(ex)}")
    status = get_first(ex, "final_status", "status", default=("fail" if steps else "unknown"))
    label = extract_label(ex)
    return {
        "id": str(rid),
        "query": query,
        "steps": steps,
        "final_status": status,
        "label": label
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="Path to Agents_Failure_Attribution/Who&When/<split>")
    ap.add_argument("--out", required=True, help="Output JSONL path")
    ap.add_argument("--print-one", action="store_true", help="Print one mapped record for debugging")
    args = ap.parse_args()

    root = Path(args.root)
    if not root.exists():
        raise SystemExit(f"not found: {root}")

    count_in, count_out = 0, 0
    printed_example = False
    with open(args.out, "w", encoding="utf-8") as w:
        for ex in iter_records_from_path(root):
            count_in += 1
            rec = map_to_ours(ex, fallback_prefix=root.name)
            if not printed_example and args.print_one:
                print("DEBUG example mapped record:\n", json.dumps(rec, indent=2, ensure_ascii=False))
                printed_example = True
            if rec["label"] is None:
                continue
            w.write(json.dumps(rec, ensure_ascii=False) + "\n")
            count_out += 1
    print(f"read {count_in} items, wrote {count_out} labeled items to {args.out}")

if __name__ == "__main__":
    main()

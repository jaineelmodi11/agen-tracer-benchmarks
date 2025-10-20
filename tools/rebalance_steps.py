#!/usr/bin/env python3
import argparse, json, random, re, sys
from collections import Counter

RNG = random.Random()

NEUTRAL_AGENTS = ["planner", "web", "coordinator"]
NEUTRAL_TEMPLATES = [
    ("planner",     "Plan next sub-task",            "ok"),
    ("web",         "Search docs for API usage",     "ok"),
    ("coordinator", "Check progress and hand-off",   "ok"),
    ("planner",     "Validate inputs are present",   "ok"),
    ("web",         "Open file / page",              "200 OK"),
    ("coordinator", "Record intermediate result",    "saved"),
]

MASKED_AGENT_NAMES = ["AgentA", "AgentB", "AgentC", "AgentD", "AgentE"]
MASK_RE = re.compile(r"^agent[a-e]$", re.IGNORECASE)

def is_masked_agent(name: str) -> bool:
    return bool(MASK_RE.match((name or "").strip()))

def pick_neutral():
    a, act, obs = RNG.choice(NEUTRAL_TEMPLATES)
    return {"t": None, "agent": a, "action": act, "obs": obs, "error": None}

def find_failure_idx0(steps):
    """First step that clearly fails."""
    if not isinstance(steps, list) or not steps:
        return None
    for i, s in enumerate(steps):
        if not isinstance(s, dict):
            continue
        # explicit error flag wins
        if s.get("error"):
            return i
        # textual error signal
        for k in ("obs", "action"):
            v = s.get(k)
            if isinstance(v, str) and re.search(
                r"(error|exception|traceback|not found|undefined|fail(ed)?|typeerror|valueerror|keyerror|zerodivision|indexerror)",
                v, re.I
            ):
                return i
    # fallback: last step
    return len(steps) - 1

def extract_failure_agent(rec, steps, fail_idx):
    lab = rec.get("label") or {}
    a = lab.get("agent")
    if a: return a
    if 0 <= fail_idx < len(steps):
        a2 = steps[fail_idx].get("agent")
        if a2: return a2
    return None

def build_variant(rec, target_idx0, seed=None, min_total_steps=3, keep_post=True):
    """
    Move the failure action to target_idx0 by constructing a new steps list:
      [NEUTRAL x target_idx0] + [FAILURE] + (optional trailing neutral)
    """
    steps = rec.get("steps") or rec.get("actions") or []
    fail_idx = find_failure_idx0(steps)
    if fail_idx is None:
        return None, None

    if seed is not None:
        RNG.seed((hash(rec.get("id")) ^ target_idx0 ^ seed) & 0xFFFFFFFF)

    failure_step = steps[fail_idx]
    # If the failure step has a masked agent, keep it; otherwise preserve canonical agent
    fail_agent = extract_failure_agent(rec, steps, fail_idx)
    if fail_agent:
        failure_step = dict(failure_step)
        failure_step["agent"] = fail_agent

    pre_neutrals = [pick_neutral() for _ in range(max(0, target_idx0))]
    new_steps = pre_neutrals + [failure_step]

    # ensure at least min_total_steps
    while len(new_steps) < min_total_steps:
        new_steps.append(pick_neutral())

    if keep_post and RNG.random() < 0.6:
        new_steps.append(pick_neutral())

    # set t fields monotonically
    for i, s in enumerate(new_steps):
        s["t"] = i

    # update record
    out = dict(rec)
    out["steps"] = new_steps
    out["actions"] = new_steps  # if your pipeline sometimes reads `actions`

    # label: keep same agent (if present), fix 0-based failure index
    lab = dict(out.get("label") or {})
    agent = extract_failure_agent(rec, steps, fail_idx)
    if agent:
        lab["agent"] = agent
    out["label"] = lab
    out["label"]["step"] = int(target_idx0)

    return out, target_idx0

def parse_targets(spec: str, total: int):
    """
    spec examples:
      "0:12,1:13,2:12,3:13"
      "equal:4"   -> spread equally across 0..3 (4 bins)
      "equal"     -> spread equally across 0..3
    """
    if not spec or spec.lower().startswith("equal"):
        bins = 4
        m = re.search(r"equal:(\d+)", spec or "", re.I)
        if m: bins = int(m.group(1))
        each = total // bins
        rem = total % bins
        targets = []
        for i in range(bins):
            n = each + (1 if i < rem else 0)
            targets += [i] * n
        return targets

    pairs = []
    for p in spec.split(","):
        k, v = p.split(":")
        pairs.append((int(k), int(v)))
    targets = []
    for k, v in pairs:
        targets += [k] * v
    # trim or pad
    if len(targets) > total:
        targets = targets[:total]
    elif len(targets) < total:
        # pad with last bin
        last = pairs[-1][0]
        targets += [last] * (total - len(targets))
    return targets

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="input JSONL")
    ap.add_argument("--out", required=True, help="output JSONL (balanced steps)")
    ap.add_argument("--targets", default="", help='e.g. "0:12,1:13,2:12,3:13" or "equal[:bins]"')
    ap.add_argument("--min-total-steps", type=int, default=3)
    ap.add_argument("--keep-post", action="store_true", help="often add a trailing neutral step")
    ap.add_argument("--seed", type=int, default=1337)
    args = ap.parse_args()

    src = [json.loads(line) for line in open(args.src, "r", encoding="utf-8") if line.strip()]
    N = len(src)
    targets = parse_targets(args.targets, N)

    out = []
    dist = Counter()
    skipped = 0

    for rec, tgt in zip(src, targets):
        newrec, idx = build_variant(
            rec,
            target_idx0=tgt,
            seed=args.seed,
            min_total_steps=args.min_total_steps,
            keep_post=args.keep_post,
        )
        if newrec is None:
            skipped += 1
            continue
        out.append(newrec)
        dist[idx] += 1

    with open(args.out, "w", encoding="utf-8") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"Wrote {len(out)} examples to {args.out} (skipped={skipped})")
    print("Failure step distribution (0-based):", dict(sorted(dist.items())))

if __name__ == "__main__":
    main()

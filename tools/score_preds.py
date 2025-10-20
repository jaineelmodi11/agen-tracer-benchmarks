#!/usr/bin/env python3
# tools/score_preds.py
import argparse, json, sys, re, collections
from typing import Dict, Optional

def parse_maskmap(s: Optional[str]) -> Dict[str, str]:
    """
    Parse a comma-separated mapping like:
      'agenta:coder,agentb:analyst,agentc:planner,agentd:web,agente:coordinator'
    Returns a dict mapping LOWERCASED keys to LOWERCASED values.
    """
    if not s:
        return {}
    m = {}
    for part in s.split(","):
        part = part.strip()
        if not part:
            continue
        if ":" not in part:
            print(f"⚠️  Ignoring bad map entry: {part}", file=sys.stderr)
            continue
        k, v = part.split(":", 1)
        m[k.strip().lower()] = v.strip().lower()
    return m

# Agent normalization (same aliases as eval)
AGENT_ALIASES = {
    "coder": {"coder", "code", "developer", "dev", "programmer"},
    "planner": {"planner", "plan"},
    "analyst": {"analyst", "reasoner", "judge"},
    "web": {"web", "web agent", "browser", "search"},
    "coordinator": {"coordinator", "coord", "orchestrator"},
}

def normalize_agent(name: Optional[str]) -> Optional[str]:
    if not name:
        return None
    s = name.strip().lower()
    s = re.sub(r"[^a-z0-9 ]+", "", s)
    for canon, aliases in AGENT_ALIASES.items():
        if s in aliases:
            return canon
    return s or None

def backmap_agent(pred: Optional[str], maskmap: Dict[str, str]) -> Optional[str]:
    """
    If prediction is a masked tag (AgentA..E), map it back to canonical agent via maskmap.
    Otherwise return normalized prediction as-is.
    """
    if pred is None:
        return None
    p = pred.strip().lower()
    # Allow both "agenta" and "agenta:" styles; also tolerate "AgentA"
    p = p.replace(":", "")
    # If present in maskmap, translate; else keep as-is
    if p in maskmap:
        return normalize_agent(maskmap[p])
    return normalize_agent(p)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preds", required=True, help="Path to predictions JSONL produced by eval.py")
    ap.add_argument(
        "--masked-map",
        type=str,
        default=None,
        help="Comma-separated back-map for masked agents, e.g. "
             "'agenta:coder,agentb:analyst,agentc:planner,agentd:web,agente:coordinator'"
    )
    args = ap.parse_args()

    maskmap = parse_maskmap(args.masked_map)

    n = agent_ok = step_ok = both_ok = 0
    by = collections.defaultdict(lambda: [0, 0, 0, 0])  # gold_agent -> [n, a_ok, s_ok, b_ok]

    with open(args.preds, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            r = json.loads(line)

            # field names supported (from eval.py variants seen in this thread)
            who_pred_raw = r.get("who_pred")
            step_pred = r.get("step_pred_idx0")
            gold_agent = r.get("label_agent") or r.get("gold_agent")
            gold_step = r.get("label_step_idx0") or r.get("gold_step_idx")

            # Back-map masked agent tags then normalize
            who_pred = backmap_agent(who_pred_raw, maskmap)
            gold_agent = normalize_agent(gold_agent)

            a_ok = (who_pred is not None and gold_agent is not None and who_pred == gold_agent)
            s_ok = (step_pred is not None and gold_step is not None and int(step_pred) == int(gold_step))
            b_ok = a_ok and s_ok

            n += 1
            agent_ok += int(a_ok)
            step_ok  += int(s_ok)
            both_ok  += int(b_ok)

            gkey = gold_agent or "unknown"
            gn, ga, gs, gb = by[gkey]
            by[gkey] = [gn + 1, ga + int(a_ok), gs + int(s_ok), gb + int(b_ok)]

    summary = {
        "samples": n,
        "agent_acc": round(agent_ok / max(1, n), 3),
        "step_acc":  round(step_ok  / max(1, n), 3),
        "both_acc":  round(both_ok  / max(1, n), 3),
    }
    print(summary)

    print("per-agent:")
    for g, (gn, ga, gs, gb) in sorted(by.items()):
        print(g, {
            "n": gn,
            "agent_acc": round(ga / max(1, gn), 3),
            "step_acc":  round(gs / max(1, gn), 3),
            "both_acc":  round(gb / max(1, gn), 3),
        })

if __name__ == "__main__":
    main()

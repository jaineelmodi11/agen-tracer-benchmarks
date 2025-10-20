#!/usr/bin/env python3
import argparse, json, random, re, sys
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional

RAND = random.Random(1337)

AGENT_POOL = ["AgentA", "AgentB", "AgentC", "AgentD", "AgentE"]

def load_jsonl(path: str) -> List[Dict[str, Any]]:
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                out.append(json.loads(line))
    return out

def dump_jsonl(path: str, rows: List[Dict[str, Any]]):
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def get_label(rec: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    lab = rec.get("label") or rec.get("labels") or rec.get("target")
    if isinstance(lab, dict):
        return {"agent": lab.get("agent"), "step": lab.get("step")}
    return None

def set_label(rec: Dict[str, Any], agent: Optional[str], step: Optional[int]):
    rec["label"] = {"agent": agent, "step": step}

def anonymize_text(s: str) -> str:
    if not isinstance(s, str):
        return s
    # simple sanitization that removes obvious code/error tokens but keeps structure
    s = re.sub(r"(?i)typeerror|valueerror|keyerror|zerodivisionerror", "Error", s)
    s = re.sub(r"[A-Za-z_][A-Za-z0-9_]*\s*\(", "FUNC(", s)  # mask function-like
    s = re.sub(r"\'[^\']*\'|\"[^\"]*\"", '"STR"', s)       # mask strings
    s = re.sub(r"\b\d+\b", "N", s)                          # mask standalone numbers
    return s

def make_decoy_like(step: Dict[str, Any]) -> Dict[str, Any]:
    # Create a no-op decoy visually similar to other actions.
    # Keep agent the same by default, so we don't leak info through agent shifts.
    agent = step.get("agent", "AgentX")
    return {
        "t":  step.get("t", 0),
        "agent": agent,
        "action": "noop()",
        "obs": "ok",
        "error": None,
    }

def renumber_ts(steps: List[Dict[str, Any]]):
    for i, s in enumerate(steps):
        s["t"] = i

def mask_agents_in_steps(steps: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], Dict[str, str]]:
    # Build a deterministic mapping from original agents to Agent[A..E]
    uniq = []
    for s in steps:
        a = s.get("agent", "")
        if a not in uniq:
            uniq.append(a)
    mp = {}
    for i, a in enumerate(uniq):
        mp[a] = AGENT_POOL[i % len(AGENT_POOL)]
    # Apply mapping
    masked = []
    for s in steps:
        s2 = dict(s)
        s2["agent"] = mp.get(s.get("agent"), "AgentX")
        masked.append(s2)
    return masked, mp

def transform_record(
    rec: Dict[str, Any],
    *,
    add_decoy: bool,
    min_actions: int,
    anonymize_actions: bool,
    mask_agents: bool,
) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """
    Returns: (withG_rec, withoutG_rec) or (None, None) if skipped.
    """
    rid = rec.get("id")
    steps = rec.get("steps") or []
    lab = get_label(rec)
    if not steps or lab is None or lab.get("step") is None:
        return None, None

    gold_idx = int(lab["step"])
    if gold_idx < 0 or gold_idx >= len(steps):
        return None, None

    # Base copy for withG (almost unchanged)
    withG = {
        k: rec[k] for k in rec.keys() if k not in {"steps", "label", "labels", "target"}
    }
    withG["id"] = rid
    withG["steps"] = [dict(s) for s in steps]
    set_label(withG, lab.get("agent"), gold_idx)

    # Build withoutG
    withoutG = {
        k: rec[k] for k in rec.keys() if k not in {"steps", "label", "labels", "target"}
    }
    withoutG["id"] = rid
    w_steps = [dict(s) for s in steps]
    w_gold = gold_idx
    w_agent = lab.get("agent")

    # Insert a decoy directly BEFORE the failure and shift the gold index
    if add_decoy:
        if 0 <= w_gold <= len(w_steps):
            decoy = make_decoy_like(w_steps[w_gold])
            w_steps.insert(w_gold, decoy)
            w_gold += 1  # CRUCIAL: label must move with the inserted step
            renumber_ts(w_steps)

    # Optionally anonymize action fields (harder)
    if anonymize_actions:
        for s in w_steps:
            s["action"] = anonymize_text(s.get("action", ""))
            s["obs"] = anonymize_text(s.get("obs", ""))
            if s.get("error"):
                s["error"] = anonymize_text(str(s.get("error")))

    # Optionally mask agents to AgentA..E (harder)
    if mask_agents:
        w_steps, agent_map = mask_agents_in_steps(w_steps)
        # also map the label agent if present (best-effort)
        if w_agent in agent_map:
            w_agent = agent_map[w_agent]
        # save the map in the record so you can reuse/inspect if needed
        withoutG["_masked_agent_map"] = agent_map

    # Enforce minimum actions (after transforms)
    if len(w_steps) < min_actions:
        return None, None

    withoutG["steps"] = w_steps
    set_label(withoutG, w_agent, w_gold)

    return withG, withoutG

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out-withG", required=True)
    ap.add_argument("--out-withoutG", required=True)
    ap.add_argument("--add-decoy", action="store_true",
                    help="Insert a no-op action *before* the failure and shift label.step by +1.")
    ap.add_argument("--min-actions", type=int, default=3)
    ap.add_argument("--anonymize-actions", action="store_true")
    ap.add_argument("--mask-agents", action="store_true",
                    help="Rename agents to AgentA..E (and map label.agent accordingly).")
    args = ap.parse_args()

    src = load_jsonl(args.src)

    withG_rows, withoutG_rows = [], []
    for rec in src:
        wg, wo = transform_record(
            rec,
            add_decoy=args.add_decoy,
            min_actions=args.min_actions,
            anonymize_actions=args.anonymize_actions,
            mask_agents=args.mask_agents,
        )
        if wg is not None and wo is not None:
            withG_rows.append(wg)
            withoutG_rows.append(wo)

    dump_jsonl(args.out_withG, withG_rows)
    dump_jsonl(args.out_withoutG, withoutG_rows)

    print(f"Wrote {len(withG_rows)} examples:")
    print(f"  with_G    -> {args.out_withG}")
    print(f"  without_G -> {args.out_withoutG}")

if __name__ == "__main__":
    main()

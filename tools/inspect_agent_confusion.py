# tools/inspect_agent_confusion.py
import argparse, json, collections

AGENTS = ("analyst", "coder", "planner", "web")

def _get_gold_agent(rec):
    for k in ("agent", "role", "target_agent"):
        if k in rec and isinstance(rec[k], str):
            return rec[k].lower().strip()
    # sometimes nested under a dict
    if isinstance(rec.get("gold"), dict) and isinstance(rec["gold"].get("agent"), str):
        return rec["gold"]["agent"].lower().strip()
    return None

def _parse_pred(s):
    toks = s.strip().split()
    if len(toks) >= 2:
        a = toks[0].lower()
        return a
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gold", required=True)
    ap.add_argument("--preds", required=True)
    args = ap.parse_args()

    gold_agents = []
    with open(args.gold, encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            a = _get_gold_agent(rec)
            if a:
                gold_agents.append(a)

    preds = []
    with open(args.preds, encoding="utf-8") as f:
        for line in f:
            a = _parse_pred(json.loads(line)["pred"])
            preds.append(a)

    assert len(gold_agents) == len(preds), "gold/preds length mismatch"

    # Confusion counts
    conf = {g: collections.Counter() for g in AGENTS}
    gold_ctr, pred_ctr, correct_ctr = collections.Counter(), collections.Counter(), 0

    for g, p in zip(gold_agents, preds):
        if g not in AGENTS: continue
        gold_ctr[g] += 1
        if p in AGENTS:
            pred_ctr[p] += 1
            conf[g][p] += 1
            if g == p: correct_ctr += 1

    # Pretty print
    print("\nGold distribution:", dict(gold_ctr))
    print("Pred distribution:", dict(pred_ctr))
    print(f"Agent accuracy: {correct_ctr / max(1,sum(gold_ctr.values())):.3f}")
    print("\nConfusion (gold → pred):")
    header = "gold\\pred".ljust(12) + "".join(x.rjust(9) for x in AGENTS)
    print(header)
    for g in AGENTS:
        row = g.ljust(12) + "".join(str(conf[g][p]).rjust(9) for p in AGENTS)
        print(row)

if __name__ == "__main__":
    main()

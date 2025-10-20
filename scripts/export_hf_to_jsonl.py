import json, argparse
from datasets import load_dataset

p = argparse.ArgumentParser()
p.add_argument("--config", choices=["Algorithm-Generated","Hand-Crafted"], required=True)
p.add_argument("--out", required=True)
args = p.parse_args()

ds = load_dataset("Kevin355/Who_and_When", args.config, split="train")
with open(args.out, "w", encoding="utf-8") as f:
    for ex in ds:
        who = None; when = None
        for cont in [ex, ex.get("label") or {}, ex.get("answer") or {}, ex.get("annotation") or {}, ex.get("who_when") or {}]:
            who  = who  or cont.get("who") or cont.get("responsible_agent") or cont.get("agent")
            when = when or cont.get("when") or cont.get("decisive_step") or cont.get("step") or cont.get("time_step")
        if when is not None:
            try:
                when = int(when)
            except:
                import re
                m = re.search(r"-?\d+", str(when))
                when = int(m.group(0)) if m else None

        steps = []
        traj = ex.get("trajectory") or []
        for t, st in enumerate(traj):
            if isinstance(st, dict):
                agent  = st.get("agent") or st.get("role") or "Agent"
                action = st.get("action") or st.get("content") or st.get("tool_input") or ""
                obs    = st.get("obs") or st.get("observation") or st.get("tool_output") or ""
                err    = st.get("error") if "error" in st else (st.get("err") or None)
            else:
                agent, action, obs, err = "Agent", str(st), "", None
            steps.append({"t": t, "agent": agent, "action": action, "obs": obs, "error": err})

        if who is None or when is None:
            continue

        rec = {
            "id": ex.get("id") or f"{args.config}_{ex.get('__index_level_0__', t)}",
            "query": ex.get("query",""),
            "steps": steps,
            "final_status": ex.get("final_status","fail"),
            "label": {"agent": str(who), "step": int(when)},
        }
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
print("wrote:", args.out)

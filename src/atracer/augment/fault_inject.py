# src/atracer/augment/fault_inject.py
import random, copy

def inject_fault(traj, rng=None):
    rng = rng or random
    t = copy.deepcopy(traj)
    k = rng.randrange(len(t["steps"]))
    step = t["steps"][k]
    role = step["role"]

    def corrupt_text(s):
        return s.replace("2018","2015") if "2018" in s else s + " !!!"

    if role in ("web","analyst","planner","coordinator"):
        step["obs"] = corrupt_text(step.get("obs",""))
        step["act"] = corrupt_text(step.get("act",""))
    else:  # coder
        step["act"] = step.get("act","") + "\n# TODO: FIXME (fault)"

    t["meta"] = {"source":"fault","fault_idx":k}
    # Error agent is *likely* this role/step (i*, t* := k)
    t["label"] = {"agent": role, "step": k}
    return t

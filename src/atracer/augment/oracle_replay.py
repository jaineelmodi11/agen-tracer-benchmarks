# src/atracer/augment/oracle_replay.py
import copy

def replay_oracle_fix(traj, fix_fn):
    """
    fix_fn(step) -> step' that is gold-consistent (your oracle).
    Returns new traj with meta.source='oracle' and decisive step t*.
    """
    t = copy.deepcopy(traj)
    for k, s in enumerate(t["steps"]):
        s_prime = fix_fn(s)
        if s_prime is None:
            continue
        t2 = copy.deepcopy(t)
        t2["steps"][k] = s_prime
        if passes_oracle(t2):  # Who&When: a lightweight rule; SWE: run tests
            t2["meta"] = {"source":"oracle","t_star":k}
            t2["label"] = {"agent": s["role"], "step": k}  # decisive step
            return t2
    return None

def passes_oracle(traj):
    # Who&When: crude check (e.g., internal “judge” LLM or regex of consistency)
    # SWE: actually run 'pytest -q' and parse exit code.
    return False

from __future__ import annotations
import copy
from dataclasses import dataclass
from typing import Protocol, Dict, Any, Optional, List, Iterable, Tuple, Sequence
import random

Traj = Dict[str, Any]

# ------------------ Interfaces ------------------

class Oracle(Protocol):
    def propose(self, traj: Traj, t: int) -> Optional[Dict[str, Any]]:
        """
        Return a rectification payload for step t (e.g., new 'action' or fields),
        or None if the oracle cannot rectify that step.
        """

class Judge(Protocol):
    def evaluate_success(self, traj: Traj) -> bool:
        """Return True iff the (possibly rectified) trajectory is considered successful (Ω(τ)=1)."""

# ------------------ Core ops ------------------

def apply_rectification(traj: Traj, t: int, patch: Dict[str, Any], *,
                        tag: str = "cfr") -> Traj:
    """
    Deterministic shallow patch:
      • deep-clones the trajectory
      • merges 'patch' into steps[t]
      • annotates metadata for traceability
      • records previous action and whether it changed
    """
    new_traj = copy.deepcopy(traj)
    steps: List[Dict[str, Any]] = list(new_traj.get("steps", []))
    if not (0 <= t < len(steps)) or not isinstance(steps[t], dict):
        return new_traj

    old_action = steps[t].get("action")
    st = steps[t]
    st["__rectified__"] = True
    st["__rectified_tag__"] = tag
    if "__prev_action" not in st:
        st["__prev_action"] = old_action

    st.update(patch)

    if "action" in patch:
        st["__action_changed__"] = (patch["action"] != old_action)
    else:
        st["__action_changed__"] = False

    new_traj["steps"] = steps
    meta = new_traj.setdefault("__cf_meta__", {})
    meta["rectified_at"] = t
    meta["rectification_patch_keys"] = sorted(patch.keys())
    return new_traj

@dataclass
class CFResult:
    found: bool
    agent: Optional[str]
    step: Optional[int]

def _extract_step_agent(s: Dict[str, Any]) -> Optional[str]:
    for k in ("agent", "role", "speaker", "who"):
        v = s.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip().lower()
    return None

def earliest_decisive_error(traj: Traj, oracle: Oracle, judge: Judge) -> CFResult:
    """
    Scan t = 0..T-1:
      1) Ask oracle for a rectification patch at t.
      2) Apply patch -> τ'
      3) If judge(τ') == success, return the FIRST such t (earliest decisive error).
    """
    steps = traj.get("steps") or []
    if not isinstance(steps, list) or not steps:
        return CFResult(False, None, None)

    for t in range(len(steps)):
        patch = oracle.propose(traj, t)
        if not patch:
            continue
        tau_prime = apply_rectification(traj, t, patch, tag="cfr-earliest")
        if judge.evaluate_success(tau_prime):
            return CFResult(True, _extract_step_agent(steps[t]), t)

    return CFResult(False, None, None)

# ------------------ Step-local CFR (tracer-first) ------------------

@dataclass
class CFRConfig:
    prefer_predicted: bool = True
    """Try the tracer-predicted failing step first if available."""
    window: int = 0
    """
    If >0, try steps in the window [k-window, k+window] around the predicted k
    before falling back to earliest_decisive_error.
    """
    rng_seed: int = 42
    """For randomized within-window ordering (stable across runs)."""

def _get_predicted_step(traj: Traj) -> Optional[int]:
    """
    Try a few common keys where a WHO/WHEN tracer might store its 'WHEN' prediction.
    """
    for k in ("pred_when", "pred_step", "predicted_step", "tracer_when", "__pred_when__", "__when__"):
        v = traj.get(k)
        if isinstance(v, int):
            return v
    # nested container?
    pred = traj.get("pred") or traj.get("__pred__") or {}
    if isinstance(pred, dict):
        v = pred.get("when") or pred.get("step")
        if isinstance(v, int):
            return v
    return None

def _valid_steps(T: int, indices: Iterable[int]) -> List[int]:
    return [t for t in indices if 0 <= t < T]

@dataclass
class CFOutcome:
    success: bool
    """judge(τ')"""
    result: CFResult
    """(found, agent, step) for the decisive error if success==True, else (False,None,None)"""
    rectified: Optional[Traj]
    """the rectified trajectory τ' if success; otherwise None"""

def counterfactual_replay_step_local(
    traj: Traj,
    oracle: Oracle,
    judge: Judge,
    *,
    config: CFRConfig = CFRConfig()
) -> CFOutcome:
    """
    Step-local CFR that **prioritizes the tracer's predicted failing step**.

    Order of attempts:
      1) If config.prefer_predicted and predicted step k exists:
         try k, and optionally steps in [k-window, k+window] (randomized but stable).
      2) Fallback to earliest_decisive_error scan.

    Returns a CFOutcome with rich metadata and the rectified τ' if success.
    """
    steps = traj.get("steps") or []
    T = len(steps)
    if not isinstance(steps, list) or T == 0:
        return CFOutcome(False, CFResult(False, None, None), None)

    tried: set[int] = set()

    # 1) predicted-first attempts
    if config.prefer_predicted:
        k = _get_predicted_step(traj)
        if isinstance(k, int):
            cand: List[int] = [k]
            if config.window > 0:
                lo, hi = k - config.window, k + config.window
                cand.extend([t for t in range(lo, hi + 1) if t != k])
            cand = _valid_steps(T, cand)

            rng = random.Random(config.rng_seed)
            rng.shuffle(cand)

            for t in cand:
                if t in tried:
                    continue
                tried.add(t)
                patch = oracle.propose(traj, t)
                if not patch:
                    continue
                tau_prime = apply_rectification(traj, t, patch, tag="cfr-predicted")
                if judge.evaluate_success(tau_prime):
                    return CFOutcome(
                        True,
                        CFResult(True, _extract_step_agent(steps[t]), t),
                        tau_prime,
                    )

    # 2) fallback to earliest decisive error
    ede = earliest_decisive_error(traj, oracle, judge)
    if ede.found and isinstance(ede.step, int):
        t = ede.step
        patch = oracle.propose(traj, t)
        tau_prime = apply_rectification(traj, t, patch or {}, tag="cfr-earliest")
        return CFOutcome(True, ede, tau_prime)

    return CFOutcome(False, CFResult(False, None, None), None)

# ------------------ Helpers / Utilities ------------------

class GoldOracle:
    """
    A simple oracle that uses ground-truth hints embedded in the trajectory.
    It looks for per-step keys: 'gold_action' or 'target_action' or 'fix_action'.
    If found, returns {'action': <that>} at t.
    """
    def __init__(self, action_keys: Sequence[str] = ("gold_action", "target_action", "fix_action")):
        self.action_keys = tuple(action_keys)

    def propose(self, traj: Traj, t: int) -> Optional[Dict[str, Any]]:
        steps = traj.get("steps") or []
        if not (0 <= t < len(steps)): return None
        st = steps[t] or {}
        for k in self.action_keys:
            if k in st and isinstance(st[k], str):
                return {"action": st[k]}
        # Fallback: if the trajectory has a global label of (agent, step), and the step holds a 'gold' field
        lab = traj.get("label") or {}
        if isinstance(lab, dict) and lab.get("step") == t and isinstance(st.get("gold"), dict):
            patch = {}
            if isinstance(st["gold"].get("action"), str):
                patch["action"] = st["gold"]["action"]
            return patch or None
        return None

class HeuristicJudge:
    """
    A permissive judge that checks a variety of 'success' spellings commonly seen
    in logs. You can wrap a real evaluator here (e.g., unit tests).
    """
    TRUE_WORDS = {"ok","pass","passed","success","succeeded","true"}
    def evaluate_success(self, traj: Traj) -> bool:
        g = traj
        # direct flags
        for k in ("passed","success","solved","fixed","win"):
            v = g.get(k)
            if isinstance(v, bool): return v
            if isinstance(v, str) and v.lower() in self.TRUE_WORDS:
                return True
        # status
        v = str(g.get("status","")).lower()
        if v in self.TRUE_WORDS: return True
        # nested result
        res = g.get("result") or g.get("metrics") or {}
        if isinstance(res, dict):
            for k in ("passed","success"):
                rv = res.get(k)
                if isinstance(rv, bool): return rv
        return False

def to_training_row_from_cf(traj: Traj, cf: CFOutcome) -> Optional[Dict[str, Any]]:
    """
    Convert a rectified outcome into a training row used by train_ppo.py:
      {prompt, gold_agent, gold_step, n_steps}
    Assumes traj has 'query' (or 'instruction'/'prompt'/'input') and 'steps' text list.
    """
    if not (cf.success and cf.result.found and isinstance(cf.result.step, int)):
        return None
    q = traj.get("query") or traj.get("instruction") or traj.get("prompt") or traj.get("input")
    steps = traj.get("steps") or []
    if not isinstance(steps, list) or not q:
        return None
    n_steps = len(steps)
    # agent:
    agent = cf.result.agent or _extract_step_agent(steps[cf.result.step] if 0 <= cf.result.step < n_steps else {}) or "coder"
    return {
        "prompt": {
            # keep raw pieces; your prompt builder can assemble
            "query": q,
            "steps": steps,
        },
        "gold_agent": agent,
        "gold_step": int(cf.result.step),
        "n_steps": int(n_steps),
        "__cf_meta__": traj.get("__cf_meta__", {}),
    }

def balanced_replay_sampler(
    trajs: Sequence[Traj],
    *,
    oracle: Oracle,
    judge: Judge,
    frac_clean: float = 1/3,
    frac_fail: float = 1/3,
    frac_cfr: float = 1/3,
    rng_seed: int = 123
) -> Dict[str, List[Traj]]:
    """
    Build a balanced mixture for training:
      • clean: judge(τ) == True
      • failing: judge(τ) == False
      • cfr: failing τ where a step-local CFR exists (predicted-first)
    Returns a dict with lists: {'clean': [...], 'fail': [...], 'cfr': [...]}
    """
    rng = random.Random(rng_seed)

    clean, fail = [], []
    for τ in trajs:
        (clean if judge.evaluate_success(τ) else fail).append(τ)

    # counterfactuals from failing
    cfr_list: List[Traj] = []
    for τ in fail:
        out = counterfactual_replay_step_local(τ, oracle, judge)
        if out.success and out.rectified is not None:
            rect = out.rectified
            rect.setdefault("__cf_meta__", {})["source"] = "cfr"
            cfr_list.append(rect)

    # sample per desired fractions
    N = len(trajs)
    n_clean = max(0, min(len(clean), round(frac_clean * N)))
    n_fail  = max(0, min(len(fail),  round(frac_fail  * N)))
    n_cfr   = max(0, min(len(cfr_list), round(frac_cfr * N)))

    rng.shuffle(clean); rng.shuffle(fail); rng.shuffle(cfr_list)

    return {
        "clean": clean[:n_clean],
        "fail":  fail[:n_fail],
        "cfr":   cfr_list[:n_cfr],
    }

# ------------------ Exports ------------------

__all__ = [
    "Traj",
    "Oracle", "Judge",
    "CFResult", "CFOutcome", "CFRConfig",
    "apply_rectification",
    "earliest_decisive_error",
    "counterfactual_replay_step_local",
    "GoldOracle", "HeuristicJudge",
    "to_training_row_from_cf",
    "balanced_replay_sampler",
]

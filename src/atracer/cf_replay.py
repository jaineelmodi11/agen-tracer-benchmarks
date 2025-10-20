from __future__ import annotations
import copy
from dataclasses import dataclass
from typing import Protocol, Dict, Any, Optional, List

Traj = Dict[str, Any]

class Oracle(Protocol):
    def propose(self, traj: Traj, t: int) -> Optional[Dict[str, Any]]:
        """
        Return a rectification payload for step t (e.g., new 'action' or fields),
        or None to indicate the oracle cannot rectify that step.
        """

class Judge(Protocol):
    def evaluate_success(self, traj: Traj) -> bool:
        """Return True iff the rectified trajectory is considered successful (Ω(τ)=1)."""

def apply_rectification(traj: Traj, t: int, patch: Dict[str, Any]) -> Traj:
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
    steps[t]["__rectified__"] = True
    if "__prev_action" not in steps[t]:
        steps[t]["__prev_action"] = old_action

    steps[t].update(patch)

    if "action" in patch:
        steps[t]["__action_changed__"] = (patch["action"] != old_action)
    else:
        # If action not in patch, mark no change explicitly
        steps[t]["__action_changed__"] = False

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
        tau_prime = apply_rectification(traj, t, patch)
        if judge.evaluate_success(tau_prime):
            return CFResult(True, _extract_step_agent(steps[t]), t)

    return CFResult(False, None, None)

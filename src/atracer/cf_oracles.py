from __future__ import annotations
from typing import Dict, Any, Optional
import re

class HeuristicOracle:
    """
    Minimal, text-based oracle to get the plumbing working:
      • If step has a probable action typo (e.g., 'pip instal'), propose FIX(patched_action).
      • Else, if step logs an error/exception, propose a generic FIX(existing_action_or_error).
    This ensures the judge can reliably detect a 'rectified' action in toy mode.
    Replace later with a domain oracle (e.g., revert/patch for SWE-bench).
    """
    _typo_fix = re.compile(r"\binstal(l?)\b", re.IGNORECASE)

    def propose(self, traj: Dict[str, Any], t: int) -> Optional[Dict[str, Any]]:
        steps = traj.get("steps") or []
        if not (0 <= t < len(steps)):
            return None
        st = steps[t] if isinstance(steps[t], dict) else {}
        action = st.get("action")

        # 1) Typo → FIX(...)
        if isinstance(action, str) and action.strip():
            fixed = self._typo_fix.sub("install", action)
            if fixed != action:
                return {"action": f"FIX({fixed})"}

        # 2) Error-ish text → FIX(...)
        for k in ("error", "exception", "traceback", "observation", "output", "message", "content"):
            v = st.get(k)
            if isinstance(v, str) and v.strip():
                src = action if isinstance(action, str) and action.strip() else v
                return {"action": f"FIX({src[:64]})"}

        # 3) Nothing to rectify
        return None

class MockJudge:
    """
    Placeholder judge for toy data:
      • If trajectory already says 'is_success' True, treat as success.
      • Else, consider it 'successful after rectification' if ANY rectified step:
          - has action starting with 'FIX('  OR
          - explicitly marked __action_changed__ == True
    Replace this with a real test-runner judge for SWE-bench.
    """
    def evaluate_success(self, traj: Dict[str, Any]) -> bool:
        if bool(traj.get("is_success")):
            return True
        for s in traj.get("steps") or []:
            a = s.get("action")
            if not s.get("__rectified__"):
                continue
            if isinstance(a, str) and a.startswith("FIX("):
                return True
            if bool(s.get("__action_changed__")):
                return True
        return False

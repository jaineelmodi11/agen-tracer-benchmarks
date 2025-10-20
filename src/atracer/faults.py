from __future__ import annotations
from typing import Dict, Any, Optional, List
import random
import re

Traj = Dict[str, Any]

class FaultInjector:
    """
    Minimal, text-safe fault injector for trajectory steps.

    Strategy:
      - If a step has an 'action' string, synthesize a failure by wrapping it in FAULT(...)
      - Else, if there is any text content (error/message/observation/etc.), wrap that.
      - Optionally add a small corruption, e.g., flip a common token ('True'->'False', '=='->'!=')

    This is intentionally conservative to avoid schema drift. Replace with a domain-specific
    injector later (e.g., mutate code edits or tool arguments).
    """

    _flip_map = [
        (re.compile(r"\bTrue\b"), "False"),
        (re.compile(r"\bFalse\b"), "True"),
        (re.compile(r"=="), "!="),
        (re.compile(r"!="), "=="),
        (re.compile(r"\bis\s+not\b"), "is"),
        (re.compile(r"\bis\b"), "is not"),
    ]

    _text_keys = ("action", "message", "content", "output", "observation", "text")

    def _first_text(self, step: Dict[str, Any]) -> Optional[str]:
        for k in self._text_keys:
            v = step.get(k)
            if isinstance(v, str) and v.strip():
                return v
        return None

    def _mutate_token(self, s: str) -> str:
        # Try a single flip; if no flip applies, return original.
        idxs = list(range(len(self._flip_map)))
        random.shuffle(idxs)
        for i in idxs:
            pat, rep = self._flip_map[i]
            if pat.search(s):
                return pat.sub(rep, s, count=1)
        return s

    def inject_into_step(self, step: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Produce a patch dict for a single step to synthesize a failure.
        Returns None if the step isn't injectable.
        """
        if not isinstance(step, dict):
            return None

        # Prefer action field
        if isinstance(step.get("action"), str) and step["action"].strip():
            mutated = self._mutate_token(step["action"])
            return {"action": f"FAULT({mutated})"}

        # Otherwise wrap the first available text-ish field
        txt = self._first_text(step)
        if txt:
            mutated = self._mutate_token(txt)
            # If there was no 'action', create one so downstream stays uniform.
            return {"action": f"FAULT({mutated})"}

        return None

    def inject_once(self, traj: Traj, k_sample: int = 3) -> tuple[Optional[Traj], Optional[Dict[str, Any]]]:
        """
        Try up to k_sample random steps; on first successful injection, return (new_traj, label).
        Label is {"agent": <agent-at-t>, "step": t} for the synthesized decisive failure.
        """
        steps = traj.get("steps") or []
        if not isinstance(steps, list) or not steps:
            return None, None

        # candidate indices
        T = len(steps)
        cand = list(range(T))
        random.shuffle(cand)
        cand = cand[:max(1, min(k_sample, T))]

        for t in cand:
            step = steps[t] if isinstance(steps[t], dict) else {}
            patch = self.inject_into_step(step)
            if patch is None:
                continue

            # clone and apply patch inline (no judge needed; we assert fail post-injection)
            new_traj = {k: v for k, v in traj.items()}
            new_steps: List[Dict[str, Any]] = [s if isinstance(s, dict) else {"content": str(s)} for s in steps]
            prev_action = new_steps[t].get("action")
            new_steps[t].update(patch)
            new_steps[t]["__fault_injected__"] = True
            new_steps[t]["__prev_action__"] = prev_action
            new_traj["steps"] = new_steps

            # mark the trajectory as failed now
            new_traj["is_success"] = False
            fi_meta = new_traj.setdefault("__fi_meta__", {})
            fi_meta["t"] = t
            fi_meta["patch_keys"] = list(patch.keys())

            # agent extraction for label
            agent = None
            for k in ("agent", "role", "speaker", "who"):
                v = step.get(k)
                if isinstance(v, str) and v.strip():
                    agent = v.strip().lower()
                    break

            label = {"agent": agent or "unknown", "step": t}
            return new_traj, label

        return None, None

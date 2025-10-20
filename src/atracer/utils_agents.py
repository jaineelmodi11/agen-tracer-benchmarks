from __future__ import annotations
import re

def canonicalize_agent(name: str | None) -> str | None:
    if not name:
        return None
    s = re.sub(r"[^a-z0-9 ]+", "", name.strip().lower())
    if s in {"coder", "code", "developer", "dev", "programmer"}:
        return "coder"
    if s in {"analyst", "reasoner", "judge"}:
        return "analyst"
    if s in {"planner", "plan"}:
        return "planner"
    if s in {"web", "browser", "search", "web agent"}:
        return "web"
    if s in {"coordinator", "coord", "orchestrator"}:
        return "coordinator"
    return s or None

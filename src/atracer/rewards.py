from __future__ import annotations
import re
from typing import Tuple, Dict, Any, Iterable, Optional

_AGENT_SET = {"coder", "analyst", "planner", "web", "coordinator"}
_AGENT_ALIASES = {"coordinator": "planner"}

def _norm(x: str | None) -> str:
    return (x or "").replace("\u00a0", " ").strip().lower()

def _canonical_agent(a: str | None) -> str:
    a = _norm(a)
    return _AGENT_ALIASES.get(a, a)

_PAT = re.compile(
    r"(?:^|\s)(coder|analyst|planner|coordinator|web)\s+(\d{1,3})(?:\s|$)",
    flags=re.IGNORECASE,
)

def parse_agent_step(
    text: str,
    *,
    allowed_agents: Optional[Iterable[str]] = None,
    pick: str = "first",
) -> Tuple[str | None, int | None]:
    allowed = { _canonical_agent(a) for a in (allowed_agents or []) if str(a).strip() }
    matches = list(_PAT.finditer(text or ""))
    if not matches:
        return None, None
    m = matches[0] if pick == "first" else matches[-1]
    a_raw, s_raw = m.group(1), m.group(2)
    a = _canonical_agent(a_raw)
    if a not in _AGENT_SET:
        return None, None
    if allowed and a not in allowed:
        return None, None
    try:
        step = int(s_raw)
    except Exception:
        return None, None
    return a, step

def compute_reward(
    output_text: str,
    gold_agent: str,
    gold_step: int,
    *,
    allowed_agents: Optional[Iterable[str]] = None,
    pick: str = "first",
    w_parse: float = 0.2,
    w_agent: float = 1.0,
    w_step_exact: float = 0.5,
    w_step_close: float = 0.2,
    close_tol: int = 1,
    w_len: float = -0.01,
) -> Dict[str, Any]:
    text = output_text or ""
    pred_agent, pred_step = parse_agent_step(text, allowed_agents=allowed_agents, pick=pick)

    parsed = (pred_agent is not None and pred_step is not None)
    R = (w_parse if parsed else -w_parse)

    if parsed:
        pa = _canonical_agent(pred_agent)
        ga = _canonical_agent(gold_agent)
        agent_reward = (w_agent if _norm(pa) == _norm(ga) else -w_agent)
        ps, gs = int(pred_step), int(gold_step)
        if ps == gs:
            step_reward = w_step_exact
        else:
            d = abs(ps - gs)
            if d <= close_tol:
                step_reward = w_step_close * (1.0 - d / max(1, close_tol))
            else:
                step_reward = -min(w_step_close, 0.2)
        R += agent_reward + step_reward
    else:
        agent_reward = 0.0
        step_reward  = 0.0

    R += w_len * max(0, len(text))

    return {
        "R": float(R),
        "format_ok": 1.0 if parsed else 0.0,
        "pred_agent": pred_agent,
        "pred_step": int(pred_step) if parsed else None,
        "agent_reward": float(agent_reward),
        "step_reward": float(step_reward),
    }

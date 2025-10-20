# src/atracer/rewards.py
from __future__ import annotations
import math, re
from typing import Tuple, Dict, Any, Iterable, Optional

# unified agent space (keep 'coordinator' as alias for planner)
_AGENT_SET = {"coder", "analyst", "planner", "web"}
_AGENT_ALIASES = {
    "coordinator": "planner",
}

def _norm(x: str | None) -> str:
    return (x or "").replace("\u00a0", " ").strip().lower()

def _canonical_agent(a: str | None) -> str:
    a = _norm(a)
    return _AGENT_ALIASES.get(a, a)

# robust "<agent> <step>" (allow multi-digit steps; allow synonyms)
_PAT = re.compile(
    r"(?:^|\s)(coder|analyst|planner|coordinator|web)\s+(\d{1,3})(?:\s|$)",
    flags=re.IGNORECASE,
)

def parse_agent_step(
    text: str,
    *,
    allowed_agents: Optional[Iterable[str]] = None,
    pick: str = "first",   # "first" or "last"
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

def _gauss_step(pred_step: Optional[int], true_step: Optional[int], sigma: float = 1.0) -> float:
    if pred_step is None or true_step is None:
        return 0.0
    d = int(pred_step) - int(true_step)
    return math.exp(- (d * d) / (2.0 * sigma * sigma))

def compute_reward(
    output_text: str,
    gold_agent: str,
    gold_step: int,
    *,
    allowed_agents: Optional[Iterable[str]] = None,
    pick: str = "first",
    # weighted scheme (your original style; default)
    w_parse: float = 0.2,        # +w if parseable, -w if not
    w_agent: float = 1.0,        # +1/-1 for agent match/mismatch
    w_step_exact: float = 0.5,   # + for exact step
    w_step_close: float = 0.2,   # partial credit if within close_tol
    close_tol: int = 1,          # distance for partial credit
    w_len: float = -0.01,        # length penalty per generated char
    # AgenTracer-style alternative (toggle on if you want)
    use_gauss: bool = False,
    sigma: float = 1.0,
    lam: float = 0.5,            # mix: lam*step_gauss + (1-lam)*agent_ok
) -> Dict[str, Any]:
    text = output_text or ""
    pred_agent, pred_step = parse_agent_step(text, allowed_agents=allowed_agents, pick=pick)
    parsed = (pred_agent is not None and pred_step is not None)

    pa = _canonical_agent(pred_agent) if pred_agent else None
    ga = _canonical_agent(gold_agent)

    agent_ok = float(pa is not None and ga and pa == ga)
    step_exact = float(pred_step is not None and int(pred_step) == int(gold_step))
    step_close = 0.0
    if pred_step is not None and not step_exact and close_tol >= 0:
        step_close = 1.0 if abs(int(pred_step) - int(gold_step)) <= int(close_tol) else 0.0

    step_gauss = _gauss_step(pred_step, gold_step, sigma=sigma)

    if use_gauss:
        # Strict format gate × mixture + length pen
        core = lam * step_gauss + (1.0 - lam) * agent_ok
        R = (1.0 if parsed else 0.0) * core + w_len * max(0, len(text))
    else:
        # Your original sign-constrained shaping
        R = (w_parse if parsed else -w_parse)
        if parsed:
            agent_reward = (w_agent if agent_ok == 1.0 else -w_agent)
            if step_exact == 1.0:
                step_reward = w_step_exact
            else:
                if step_close == 1.0:
                    d = abs(int(pred_step) - int(gold_step))
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
        "agent_ok": agent_ok,
        "step_exact": step_exact,
        "step_close": step_close,
        "step_gauss": step_gauss,
        "len": len(text),
    }

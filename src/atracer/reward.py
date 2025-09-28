from __future__ import annotations
import math
from typing import Dict, Any
from .prompts import has_valid_format, parse_answer

def normalize_agent(a: str) -> str:
    a = a.strip().lower()
    aliases = {
        "agenta":"coder", "agentb":"analyst",
        "agentc":"planner", "agentd":"web", "agente":"coordinator"
    }
    return aliases.get(a, a)

def compute_reward(
    output_text: str,
    gold_agent: str,
    gold_step_idx0: int,
    lam: float = 0.5,
    sigma: float = 1.0
) -> Dict[str, Any]:
    # 0) format gate
    if not has_valid_format(output_text):
        return {"R": 0.0, "ok": 0, "r_agent": 0.0, "r_step": 0.0}

    parsed = parse_answer(output_text)
    if not parsed:
        return {"R": 0.0, "ok": 0, "r_agent": 0.0, "r_step": 0.0}

    pred_agent_raw, pred_step = parsed
    pred_agent = normalize_agent(pred_agent_raw)
    gold_agent = normalize_agent(gold_agent)

    # 1) agent term
    r_agent = 1.0 if pred_agent == gold_agent else 0.0

    # 2) step term (Gaussian around gold step)
    diff = float(pred_step - int(gold_step_idx0))
    r_step = math.exp(- (diff * diff) / (2.0 * sigma * sigma))

    # 3) total reward
    R = lam * r_step + (1.0 - lam) * r_agent
    return {"R": R, "ok": 1, "r_agent": r_agent, "r_step": r_step,
            "pred_agent": pred_agent, "pred_step": int(pred_step)}

# src/atracer/prompts.py
from __future__ import annotations
from typing import List

AGENTS = ("analyst", "coder", "planner", "web")  # coordinator is treated as planner

def _format_steps(steps: List[str]) -> str:
    clean = []
    for i, s in enumerate(steps):
        t = s.strip() if isinstance(s, str) else str(s).strip()
        clean.append(f"{i+1}. {t}" if t else f"{i+1}. (empty)")
    return "\n".join(clean) if clean else "(no steps provided)"

def build_eval_prompt(query: str, steps: List[str]) -> str:
    """
    Build the evaluation prompt for FAILURE ATTRIBUTION:
    Given the query and the multi-step trace, output the (agent, step) that most likely FAILED.
    Model MUST reply with exactly one line: "<Agent> <Step>"
    where Agent ∈ {Analyst, Coder, Planner, Web} and Step is 1-based.
    """
    return (
        "You are given a query and a multi-step trace. Identify the (agent, step) that most likely failed.\n\n"
        "Trace:\n"
        f"{_format_steps(steps)}\n\n"
        f"Query:\n{query.strip()}\n\n"
        "Answer with EXACTLY one line: '<Agent> <Step>' where Agent is one of "
        "{Analyst, Coder, Planner, Web} and Step is a 1-based integer. No extra words."
    )

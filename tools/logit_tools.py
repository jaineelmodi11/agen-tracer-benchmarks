# src/atracer/logit_tools.py
from __future__ import annotations
import re
from typing import Dict, List, Optional, Iterable

import torch
from transformers import LogitsProcessor, StoppingCriteria

# Broader agent surface (you can trim via --allowed-agents at runtime)
PAIR_RE = re.compile(
    r"\b(analyst|coder|planner|tester|retriever|coordinator|web)\b\D{0,10}(\d{1,3})\b",
    re.IGNORECASE,
)

def first_piece_ids(tok, text: str) -> List[int]:
    """Return candidate first-piece token ids for a word like 'Analyst' or 'Coder'."""
    ids = set()
    for s in (text, " " + text, text.lower(), " " + text.lower()):
        enc = tok.encode(s, add_special_tokens=False)
        if enc:
            ids.add(enc[0])
    return sorted(ids)

def build_agent_token_map(tok, allowed_agents: Iterable[str]) -> Dict[str, List[int]]:
    out: Dict[str, List[int]] = {}
    for a in allowed_agents:
        key = a.strip().lower()
        out[key] = first_piece_ids(tok, a.strip())
    return out


class FirstTokenRestrictor(LogitsProcessor):
    """
    At generation step 0:
      - restrict logits to first-piece tokens that can start one of the allowed agent words
      - optionally add small per-token logit bumps (bias) for nudging
    """
    def __init__(
        self,
        prompt_len: int,
        tok,
        allowed_agents: List[str],
        agent_token_map: Dict[str, List[int]],
        bias: Optional[Dict[int, float]] = None,
    ):
        self.prompt_len = prompt_len
        self.allowed = {a.lower() for a in (allowed_agents or [])}
        self.agent_token_map = agent_token_map
        self.bias = bias or {}

        self.allowed_ids = set()
        if self.allowed:
            for a in self.allowed:
                for tid in self.agent_token_map.get(a, []):
                    self.allowed_ids.add(tid)

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor) -> torch.FloatTensor:
        step = input_ids.shape[1] - self.prompt_len
        if step == 0 and self.allowed_ids:
            mask = torch.full_like(scores, float("-inf"))
            mask[:, list(self.allowed_ids)] = 0.0
            scores = scores + mask
            if self.bias:
                for tid, bump in self.bias.items():
                    scores[:, tid] += bump
        return scores


class StopOnFirstPair(StoppingCriteria):
    """Stop as soon as a valid '(Agent, Step)' appears among the allowed agents."""
    def __init__(self, tok, prompt_len: int, allowed=None):
        super().__init__()
        self.tok = tok
        self.prompt_len = prompt_len
        self.allowed = {a.strip().lower() for a in (allowed or [])}

    def __call__(self, input_ids, scores, **kwargs) -> bool:
        gen = input_ids[0][self.prompt_len:].tolist()
        if not gen:
            return False
        text = self.tok.decode(gen, skip_special_tokens=True)
        for m in PAIR_RE.finditer(text):
            a = m.group(1).lower()
            if not self.allowed or a in self.allowed:
                return True
        return False

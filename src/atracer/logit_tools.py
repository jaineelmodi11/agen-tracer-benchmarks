# src/atracer/logit_tools.py
from __future__ import annotations
import re
from typing import Dict, List, Iterable, Optional

import torch
from transformers import LogitsProcessor, StoppingCriteria

# Regex used across eval/train to detect "<agent> ... <step>"
PAIR_RE = re.compile(r"\b(analyst|coder|planner|web|coordinator)\b\D{0,10}(\d{1,3})\b", re.I)

# ---------- Token helpers ----------

def _first_piece_ids(tok, text: str) -> List[int]:
    """
    Return candidate first-piece token ids for a word like 'Analyst' or 'Coder',
    considering with/without leading space and lower-case forms.
    """
    ids = set()
    for s in (text, " " + text, text.lower(), " " + text.lower()):
        enc = tok.encode(s, add_special_tokens=False)
        if enc:
            ids.add(enc[0])
    return sorted(ids)

def build_agent_token_map(tok, allowed_agents: Iterable[str]) -> Dict[str, List[int]]:
    out: Dict[str, List[int]] = {}
    for a in allowed_agents or []:
        key = a.strip().lower()
        if not key:
            continue
        out[key] = _first_piece_ids(tok, a.strip())
    return out

def _number_first_piece_ids(tok, numbers: Iterable[int]) -> List[int]:
    ids = set()
    for n in numbers:
        s = str(int(n))
        for t in (s, " " + s):
            enc = tok.encode(t, add_special_tokens=False)
            if enc:
                ids.add(enc[0])
    return sorted(ids)

# ---------- Logits processors & stopping ----------

class FirstTokenRestrictor(LogitsProcessor):
    """
    At generation step 0:
      - restrict logits to first-piece tokens that can start one of the allowed agent words
      - optionally add a small bias toward certain agent starts (e.g., Coder vs Analyst)
    """
    def __init__(
        self,
        prompt_len: int,
        tok,
        allowed_agents: Iterable[str],
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


class StepDigitRestrictor(LogitsProcessor):
    """
    EAGER digit restrictor (legacy): immediately after start, force next token(s)
    toward digits for 1..n_steps. This can over-constrain if the agent token
    hasn't actually been chosen yet.
    """
    def __init__(self, prompt_len: int, tok, n_steps: int):
        self.prompt_len = prompt_len
        self.allowed_num_ids = set(_number_first_piece_ids(tok, range(1, max(1, int(n_steps)) + 1)))
        # allow common whitespace/sep so we don't block ' coder 1' vs 'coder 1'
        self.allowed_misc = set()
        for s in [" ", "\n"]:
            enc = tok.encode(s, add_special_tokens=False)
            if enc:
                self.allowed_misc.add(enc[0])

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor) -> torch.FloatTensor:
        gen_step = input_ids.shape[1] - self.prompt_len
        if gen_step in (1, 2, 3) and self.allowed_num_ids:
            allowed = list(self.allowed_num_ids | self.allowed_misc)
            mask = torch.full_like(scores, float("-inf"))
            mask[:, allowed] = 0.0
            scores = scores + mask
        return scores


class AgentThenStepRestrictor(LogitsProcessor):
    """
    SAFER digit restrictor: only after the *first generated token* is an agent
    start piece, constrain the next 1–2 positions to digits in 1..n_steps
    (allowing a single whitespace/newline).
    """
    def __init__(self, prompt_len: int, tok, agent_start_ids: Iterable[int], n_steps: int):
        self.prompt_len = prompt_len
        self.agent_start_ids = set(int(t) for t in agent_start_ids)
        self.allowed_num_ids = set(_number_first_piece_ids(tok, range(1, max(1, int(n_steps)) + 1)))
        self.allowed_misc = set()
        for s in [" ", "\n"]:
            enc = tok.encode(s, add_special_tokens=False)
            if enc:
                self.allowed_misc.add(enc[0])

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor) -> torch.FloatTensor:
        gen = input_ids[0][self.prompt_len:]
        if gen.numel() == 0:
            return scores

        first_tok = int(gen[0].item())
        if first_tok not in self.agent_start_ids:
            # Don't constrain until we've actually emitted the agent start token.
            return scores

        # Once the agent token is chosen, steer the next 1–2 positions to digits / whitespace.
        gen_step = gen.numel()  # number of generated tokens so far
        if gen_step in (1, 2) and self.allowed_num_ids:
            allowed = list(self.allowed_num_ids | self.allowed_misc)
            mask = torch.full_like(scores, float("-inf"))
            mask[:, allowed] = 0.0
            scores = scores + mask
        return scores


class StopOnFirstPair(StoppingCriteria):
    def __init__(self, tok, prompt_len: int, allowed: Optional[Iterable[str]] = None):
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


__all__ = [
    "PAIR_RE",
    "FirstTokenRestrictor",
    "StepDigitRestrictor",
    "AgentThenStepRestrictor",
    "StopOnFirstPair",
    "build_agent_token_map",
    "_first_piece_ids",
]

from __future__ import annotations
import argparse, json, re
from typing import List

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, LogitsProcessorList, StoppingCriteriaList

from src.atracer.logit_tools import (
    FirstTokenRestrictor,
    StepDigitRestrictor,
    AgentThenStepRestrictor,
    StopOnFirstPair,
    build_agent_token_map,
    _first_piece_ids,
    PAIR_RE,
)

def _score_prompt_is_codey(prompt: str) -> float:
    needles = [
        r"```", r"\bdef\b", r"\bclass\b", r"\bimport\b", r"\breturn\b", r"\bfunction\b",
        r"\btraceback\b", r"\bstack\s*trace\b", r"\berror:\b", r"\bunit\s*test\b",
        r"\bpytest\b", r"\bassert\b",
    ]
    hits = sum(bool(re.search(rx, prompt, re.I)) for rx in needles)
    return min(1.0, hits / 3.0)

def _read_jsonl(path: str):
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for ln in f:
            if ln.strip():
                out.append(json.loads(ln))
    return out

def _build_prompt(q, steps) -> str:
    lines = ["You are given a query and a multi-step trace. Identify the (agent, step) that most likely failed.",
             "",
             "Trace:"]
    for i, s in enumerate(steps, 1):
        lines.append(f"{i}. {s}")
    lines.append("")
    lines.append(f"Query: {q}")
    lines.append("")
    lines.append("Answer with 'Analyst N' or 'Coder N' or 'Planner N' or 'Web N'.")
    return "\n".join(lines)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--tokenizer", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--save", required=True)

    ap.add_argument("--device", default="")
    ap.add_argument("--max-input", type=int, default=320)
    ap.add_argument("--allowed-agents", default="analyst,coder,planner,web")
    ap.add_argument("--silence-warnings", action="store_true")
    ap.add_argument("--no-chat-template", action="store_true")
    ap.add_argument("--pick", default="first", choices=["first"])
    ap.add_argument("--stopping", default="first_pair", choices=["first_pair"])
    ap.add_argument("--cut-after-first-pair", action="store_true")
    ap.add_argument("--max-new", type=int, default=24)
    ap.add_argument("--step-gate", default="safe", choices=["safe", "eager", "none"])
    args = ap.parse_args()

    device = args.device or ("mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu")

    tok = AutoTokenizer.from_pretrained(args.tokenizer, trust_remote_code=True)
    if tok.pad_token_id is None:
        tok.pad_token = tok.eos_token
    tok.truncation_side = "left"
    tok.padding_side = "left"

    model = AutoModelForCausalLM.from_pretrained(args.model, trust_remote_code=True).to(device)

    data = _read_jsonl(args.data)
    allowed = [a.strip().lower() for a in (args.allowed_agents or "").split(",") if a.strip()]
    agent_token_map = build_agent_token_map(tok, allowed) if allowed else {}
    agent_start_ids = set()
    for a in allowed:
        for tid in _first_piece_ids(tok, a):
            agent_start_ids.add(tid)

    out_lines: List[str] = []

    for row in data:
        q = row.get("query") or row.get("instruction") or row.get("prompt") or row.get("input") or ""
        steps = row.get("steps") or row.get("trace") or row.get("rationale") or []
        if not q or not steps:
            out_lines.append("")
            continue

        prompt = _build_prompt(q, steps)
        enc = tok(prompt, return_tensors="pt", truncation=True, padding=True, max_length=args.max_input).to(device)
        input_ids = enc["input_ids"]; attention_mask = enc["attention_mask"]
        prompt_len = input_ids.shape[1]

        # prior bias
        bias = {}
        if allowed:
            codeyness = _score_prompt_is_codey(prompt)
            coder_boost = 2.0 * codeyness
            analyst_boost = 1.2 * (1.0 - codeyness)
            for tid in agent_token_map.get("coder", []):
                bias[tid] = bias.get(tid, 0.0) + coder_boost
            for tid in agent_token_map.get("analyst", []):
                bias[tid] = bias.get(tid, 0.0) + analyst_boost

        procs = LogitsProcessorList()
        if allowed:
            procs.append(
                FirstTokenRestrictor(
                    prompt_len=prompt_len,
                    tok=tok,
                    allowed_agents=allowed,
                    agent_token_map=agent_token_map,
                    bias=bias,
                )
            )

        if args.step_gate == "eager":
            procs.append(StepDigitRestrictor(prompt_len=prompt_len, tok=tok, n_steps=len(steps)))
        elif args.step_gate == "safe":
            procs.append(AgentThenStepRestrictor(prompt_len=prompt_len, tok=tok, agent_start_ids=agent_start_ids, n_steps=len(steps)))
        # else: none

        stops = StoppingCriteriaList([StopOnFirstPair(tok, prompt_len, allowed=allowed)])

        with torch.no_grad():
            result = model.generate(
                input_ids=input_ids, attention_mask=attention_mask,
                max_new_tokens=args.max_new, do_sample=False,
                temperature=None, top_p=None, top_k=None, typical_p=None, penalty_alpha=None,
                logits_processor=procs if len(procs) > 0 else None,
                stopping_criteria=stops,
                pad_token_id=tok.pad_token_id, eos_token_id=tok.eos_token_id,
                return_dict_in_generate=True,
            )

        cont = result.sequences[0][prompt_len:].tolist()
        text = tok.decode(cont, skip_special_tokens=True)

        # pick first (agent, step)
        m = None
        for mm in PAIR_RE.finditer(text):
            a = mm.group(1).lower()
            if not allowed or a in allowed:
                m = mm; break

        out_lines.append("" if m is None else f"{m.group(1).capitalize()} {int(m.group(2))}")

    with open(args.save, "w", encoding="utf-8") as f:
        for ln in out_lines:
            f.write((ln or "").strip() + "\n")

    print(f"Wrote {len(out_lines)} lines to {args.save}")


if __name__ == "__main__":
    main()

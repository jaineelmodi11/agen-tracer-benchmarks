# atracer/training/ppo_with_tracer.py
from dataclasses import dataclass
from typing import Dict, Any, Optional
import torch
import torch.nn as nn

from transformers import AutoModelForCausalLM, AutoTokenizer
# If you use TRL, import PPOTrainer/Config; otherwise integrate with your PPO loop.
# from trl import PPOConfig, PPOTrainer

from atracer.models.tracer_head import TracerHead

@dataclass
class TracerCfg:
    n_when_classes: int = 33      # 32 steps + no-fail
    who_weight: float = 1.0
    when_weight: float = 1.0
    lambda_tracer: float = 0.2    # scales aux loss in PPO
    label_smoothing: float = 0.0

class PolicyWithTracer(nn.Module):
    """
    Thin wrapper: exposes an LM and a tracer head.
    """
    def __init__(self, lm: AutoModelForCausalLM, hidden_size: int, tracer_cfg: TracerCfg):
        super().__init__()
        self.lm = lm
        self.tracer = TracerHead(hidden_size, tracer_cfg.n_when_classes)
        self.tr_cfg = tracer_cfg

    def pooled(self, last_hidden_state: torch.Tensor, attention_mask: Optional[torch.Tensor]=None):
        # Simple pooling: last token hidden state (works for now; can switch to step-aware later)
        return last_hidden_state[:, -1, :]

    def tracer_loss_from_batch(self, lm_outputs, batch: Dict[str, torch.Tensor]) -> torch.Tensor:
        # lm_outputs must include hidden_states; ensure LM was called with output_hidden_states=True
        h = lm_outputs.hidden_states[-1]                # [B, T, H]
        pooled = self.pooled(h, batch.get("attention_mask"))
        out = self.tracer(
            pooled,
            who_labels=batch.get("who_labels"),
            when_labels=batch.get("when_labels"),
            who_weight=self.tr_cfg.who_weight,
            when_weight=self.tr_cfg.when_weight,
            label_smoothing=self.tr_cfg.label_smoothing,
        )
        return out.loss if out.loss is not None else torch.tensor(0.0, device=pooled.device)

def add_tracer_aux_to_ppo_loss(
    model: PolicyWithTracer,
    ppo_loss: torch.Tensor,
    lm_outputs,
    batch: Dict[str, torch.Tensor],
) -> torch.Tensor:
    aux = model.tracer_loss_from_batch(lm_outputs, batch)
    return ppo_loss + model.tr_cfg.lambda_tracer * aux

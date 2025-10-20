from typing import Dict, Any, List
import json
from torch.utils.data import Dataset
from .schema import Record, Step
from .prompts import build_prompt

class JsonlAttributionDataset(Dataset):
    def __init__(self, path: str):
        self.records: List[Record] = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                obj = json.loads(line)
                obj["steps"] = [Step(**s) for s in obj["steps"]]
                self.records.append(Record(**obj))

    def __len__(self):
        return len(self.records)

    def __getitem__(self, idx: int) -> Dict[str, Any]:
        rec = self.records[idx]
        prompt = build_prompt(rec)
        target_agent = rec.label["agent"] if rec.label else ""
        target_step = rec.label["step"] if rec.label else -1
        target = f"<think>Reasoning...</think>\n<answer>{target_agent} | {target_step}</answer>"
        return {"prompt": prompt, "target": target, "meta": rec.model_dump()}

# Preview how a JSONL record renders into the training prompt
import json, argparse
from src.atracer.schema import Record
from src.atracer.prompts import build_prompt

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--jsonl", required=True)
    p.add_argument("--n", type=int, default=1)
    args = p.parse_args()
    with open(args.jsonl, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= args.n: break
            rec = Record(**json.loads(line))
            print(build_prompt(rec))

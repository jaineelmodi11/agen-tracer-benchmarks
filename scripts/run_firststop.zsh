#!/usr/bin/env zsh
set -euo pipefail
setopt interactivecomments; unsetopt BANG_HIST

: ${DATA_WITH:?"Set DATA_WITH=/abs/path/to/withG.tail2.jsonl"}
: ${DATA_WITHOUT:?"Set DATA_WITHOUT=/abs/path/to/withoutG.tail2.jsonl"}

flags=(
  --no-chat-template --allow-robust --silence-warnings
  --bias planner=-2.0 --bias analyst=-0.5 --bias coder=+4.0
  --bias-scope first --restrict-first-agent
  --pick first --stopping first_pair --cut-after-first-pair
  --device mps --max-input 384 --max-new 24
)

tcase() {
  local in="$1"; local out="${in%.jsonl}.Tcase.jsonl"
  python - <<'PY' "$in" "$out"
import json, sys
inp, outp = sys.argv[1], sys.argv[2]
case_map = {'analyst':'Analyst','coder':'Coder','planner':'Planner','web':'Web'}
with open(inp, encoding='utf-8') as f, open(outp, 'w', encoding='utf-8') as o:
    for line in f:
        if not line.strip(): continue
        rec = json.loads(line)
        agent, step = rec['pred'].split()
        rec['pred'] = f"{case_map.get(agent, agent)} {step}"
        json.dump(rec, o); o.write("\n")
print(outp)
PY
}

for CK in checkpoints/atracer-ppo-qwen0p5b-fixed/epoch00-*; do
  tag=$(basename "$CK")
  OUT_WITH="/tmp/${tag}.withG.firststop.jsonl"
  OUT_WO="/tmp/${tag}.withoutG.firststop.jsonl"

  echo "== ${tag} (WITH G) =="
  PYTHONPATH=$PWD python tools/eval_dump_min.py \
    --model "$CK" --tokenizer "$CK" \
    --data "$DATA_WITH" --save "$OUT_WITH" \
    "${flags[@]}"
  OUT_WITH_T=$(tcase "$OUT_WITH")
  python tools/score_preds_robust.py \
    --preds "$OUT_WITH_T" --gold "$DATA_WITH" --gold-remapped

  echo "== ${tag} (WITHOUT G) =="
  PYTHONPATH=$PWD python tools/eval_dump_min.py \
    --model "$CK" --tokenizer "$CK" \
    --data "$DATA_WITHOUT" --save "$OUT_WO" \
    "${flags[@]}"
  OUT_WO_T=$(tcase "$OUT_WO")
  python tools/score_preds_robust.py \
    --preds "$OUT_WO_T" --gold "$DATA_WITHOUT" --gold-remapped
done

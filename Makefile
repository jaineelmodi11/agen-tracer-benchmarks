PY := python
MODEL_BASE := Qwen/Qwen2.5-0.5B-Instruct
OUT := checkpoints/atracer-qwenrl-0p5b
DATA_TRAIN := data/tracer_like.train.tiny.jsonl
DATA_VAL   := data/tracer_like.val.tiny.jsonl
DATA_TESTG := data/who_when.test.withG.jsonl
DATA_TESTH := data/who_when.test.withoutG.hardened.jsonl

MPS_ENV := ACCELERATE_USE_MPS_DEVICE=1 PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0

.PHONY: train best eval-trainfmt eval-hardened eval-paper sweep clean

train:
	$(MPS_ENV) $(PY) -m src.atracer.rl_train \
	  --model "$(MODEL_BASE)" \
	  --train $(DATA_TRAIN) \
	  --val   $(DATA_VAL) \
	  --out   $(OUT) \
	  --batch 1 --lr 1e-6 \
	  --epochs 16 \
	  --max_new_tokens 24 \
	  --updates 64 \
	  --save-every 8 \
	  --lam 0.8 \
	  --sigma 0.8

best:
	mkdir -p $(OUT)
	ln -sfn $(OUT)/epoch15-upd064 $(OUT)/best || true

eval-trainfmt:
	$(PY) -m src.atracer.eval --trainfmt \
	  --model $(OUT)/best \
	  --data  $(DATA_TESTG) \
	  --device mps \
	  --max-input-tokens 384 --max-new-tokens 64 \
	  --save-preds checkpoints/qwenrl0p5b.trainfmt.withG.jsonl

eval-hardened:
	$(PY) -m src.atracer.eval --trainfmt \
	  --model $(OUT)/best \
	  --data  $(DATA_TESTH) \
	  --device mps \
	  --max-input-tokens 384 --max-new-tokens 64 \
	  --save-preds checkpoints/qwenrl0p5b.trainfmt.withoutG.jsonl

# curiosity only — different prompt style
eval-paper:
	$(PY) -m src.atracer.eval \
	  --paper-like \
	  --model $(OUT)/best \
	  --data  $(DATA_TESTG) \
	  --device mps \
	  --max-input-tokens 384 --max-new-tokens 64 \
	  --save-preds checkpoints/qwenrl0p5b.paper.withG.jsonl

sweep:
	for ck in epoch01-upd008 epoch07-upd032 epoch15-upd064; do \
	  $(PY) -m src.atracer.eval --trainfmt \
	    --model $(OUT)/$$ck \
	    --data $(DATA_TESTG) \
	    --device mps --max-input-tokens 384 --max-new-tokens 64 \
	    --save-preds checkpoints/preds_evalpy_$$ck.jsonl ; \
	done

clean:
	rm -f checkpoints/*.jsonl

# AgenTracer Benchmarks

This repo collects evaluation artifacts and scripts for:
- **Who&When** benchmark
- **Coding** benchmark (dataset TBD)
- **SWE-bench Lite**

It also contains baseline comparisons and slide assets.

## Layout
- `who_when/` – predictions & gold + evaluator
- `coding/` – predictions & (gold|harness) + evaluator
- `swebench/` – `preds.fixed.jsonl`, `runs/*.json`, logs, and aggregator
- `baselines/` – baseline predictions to compare head-to-head
- `scripts/` – small evaluators & aggregators
- `slides/` – final deck output (to be added later)

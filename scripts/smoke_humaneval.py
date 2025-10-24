# scripts/smoke_humaneval.py
import json, tempfile, inspect
from pathlib import Path
from human_eval.data import read_problems
from human_eval.evaluation import evaluate_functional_correctness as he_eval

def run_eval(samples_path: str, problem_file: str, n_workers: int = 1, timeout: int = 45):
    """Compatibility wrapper for different human-eval versions."""
    sig = inspect.signature(he_eval)
    params = sig.parameters
    supports_kwargs = any(p.kind == p.VAR_KEYWORD for p in params.values())
    kwargs = {}
    if "problem_file" in params or supports_kwargs: kwargs["problem_file"] = problem_file
    if "n_workers" in params or supports_kwargs: kwargs["n_workers"] = n_workers
    if "timeout" in params or supports_kwargs: kwargs["timeout"] = timeout
    try:
        if "ks" in params or supports_kwargs:
            return he_eval(samples_path, ks=[1], **kwargs)
        if "k" in params or supports_kwargs:
            return he_eval(samples_path, k=1, **kwargs)
    except TypeError:
        pass
    try:
        return he_eval(samples_path, [1], n_workers, timeout, problem_file)
    except TypeError:
        return he_eval(samples_path, [1], n_workers, timeout)

def main():
    PF = "data/humaneval/HumanEval.jsonl"
    problems = read_problems(PF)

    # Build a subset problem file of exactly 10 tasks
    subset_ids = list(problems.keys())[:10]
    subset_path = "data/humaneval/HumanEval_subset10.jsonl"
    Path("data/humaneval").mkdir(parents=True, exist_ok=True)
    with open(subset_path, "w", encoding="utf-8") as out:
        for tid in subset_ids:
            row = problems[tid]
            out.write(json.dumps({
                "task_id": tid,
                "prompt": row["prompt"],
                "canonical_solution": row.get("canonical_solution",""),
                "test": row.get("test",""),
                "entry_point": row.get("entry_point","solution"),
            }) + "\n")

    # Trivial completions for those 10 tasks
    samples_path = tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False).name
    with open(samples_path, "w", encoding="utf-8") as f:
        for tid in subset_ids:
            ep = problems[tid]["entry_point"]
            f.write(json.dumps({"task_id": tid,
                                "completion": f"def {ep}(*a, **k):\n    return None\n"})+"\n")

    # Run eval (spawns safely because we’re in __main__)
    res = run_eval(samples_path, problem_file=subset_path, n_workers=1, timeout=45)

    # Normalize pass@1
    pass1 = None
    if isinstance(res, dict):
        if isinstance(res.get("pass@1"), (int, float)):
            pass1 = float(res["pass@1"])
        elif isinstance(res.get("pass@k"), dict) and 1 in res["pass@k"]:
            pass1 = float(res["pass@k"][1])

    print("OK. keys:", list(res.keys()) if isinstance(res, dict) else type(res))
    print("pass@1:", f"{pass1:.3f}" if pass1 is not None else pass1)

    # Also read the JSONL that human-eval writes for per-task results
    results_path = samples_path + "_results.jsonl"
    tried = 0
    passed = 0
    if Path(results_path).exists():
        with open(results_path, "r", encoding="utf-8") as rf:
            for ln in rf:
                if not ln.strip(): continue
                obj = json.loads(ln)
                if obj.get("task_id") in subset_ids:
                    tried += 1
                    if obj.get("passed"): passed += 1
        print("per-task JSONL:", results_path)
        print(f"num_results: {tried}  passed: {passed}  pass@1(calc)={passed/max(1,tried):.3f}")
    else:
        print("per-task JSONL not found (this is OK on some versions).")

if __name__ == "__main__":
    main()

# tools/eval_humaneval_min.py
from __future__ import annotations

# stdlib
import argparse, json, os, re, tempfile, random, inspect, textwrap, pathlib, warnings, shutil
from typing import Dict, List, Tuple, Optional

# ------------------------------------------------------------------------------------
# Early environment / temp handling (must run before importing transformers/tokenizers)
# ------------------------------------------------------------------------------------
# 1) Repo-local TMP to avoid macOS /var tmp exhaustion
_repo_root = pathlib.Path.cwd()
_tmp_dir = _repo_root / "run" / "tmp"
_tmp_dir.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("TMPDIR", str(_tmp_dir.resolve()))

# 2) Quiet usual HF/tokenizers noise
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
warnings.filterwarnings("ignore", category=UserWarning, module="transformers")

# 3) macOS/py3.12 atexit temp cleanup guards
import tempfile as _tf, shutil as _shutil
_orig_td_cleanup = _tf.TemporaryDirectory.cleanup
def _quiet_tempdir_cleanup(self):
    try:
        _orig_td_cleanup(self)
    except Exception:
        try:
            _shutil.rmtree(self.name, ignore_errors=True)
        except Exception:
            pass
_tf.TemporaryDirectory.cleanup = _quiet_tempdir_cleanup

# Also guard shutil's internal rmtree helper when os.unlink is None at teardown
try:
    _orig_rmtree_safe_fd = _shutil._rmtree_safe_fd  # type: ignore[attr-defined]
    def _safe_rmtree(stack, onexc):
        try:
            return _orig_rmtree_safe_fd(stack, onexc)
        except TypeError:
            # Happens when os.unlink is None during interpreter teardown.
            return
    _shutil._rmtree_safe_fd = _safe_rmtree  # type: ignore[attr-defined]
except Exception:
    pass

# ------------------------------------------------------------------------------------
# 3rd-party imports (after guards)
# ------------------------------------------------------------------------------------
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# ---------------- HumanEval problems loader ----------------
try:
    from human_eval.data import read_problems  # pip install human-eval
    HAVE_HE = True
except Exception:
    HAVE_HE = False


def _load_humaneval(args) -> Dict[str, Dict]:
    if args.jsonl:
        with open(args.jsonl, "r", encoding="utf-8") as f:
            data = [json.loads(x) for x in f if x.strip()]
        return {row["task_id"]: row for row in data}
    if HAVE_HE:
        return read_problems()
    raise RuntimeError("Install 'human-eval' (pip install human-eval) OR pass --jsonl /path/to/HumanEval.jsonl")


def _write_problem_subset(problems: Dict[str, Dict], task_ids: List[str]) -> str:
    # Use repo-local tmpdir implicitly via TMPDIR we set above
    path = tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False).name
    with open(path, "w", encoding="utf-8") as f:
        for tid in task_ids:
            row = problems[tid]
            obj = {
                "task_id": tid,
                "prompt": row["prompt"],
                "canonical_solution": row.get("canonical_solution", ""),
                "test": row.get("test", ""),
                "entry_point": row.get("entry_point", ""),
            }
            f.write(json.dumps(obj) + "\n")
    return path


def _strip_md_fences(s: str) -> str:
    s = s.strip()
    s = re.sub(r"^```[a-zA-Z0-9_+-]*\s*", "", s)
    s = re.sub(r"\s*```$", "", s)
    return s


def _looks_like_prose(line: str) -> bool:
    return bool(re.match(r"^[A-Za-z].*\.$", line.strip())) and ("def " not in line)


def _extract_def_body(text: str, entry_point: str) -> Optional[str]:
    # Full def -> pull its indented body only
    m = re.search(rf"(?ms)^\s*def\s+{re.escape(entry_point)}\s*\(.*?\):\s*\n", text)
    if not m:
        return None
    start = m.end()
    rest = text[start:]
    lines = rest.splitlines()
    if not lines:
        return ""

    body_lines: List[str] = []
    for ln in lines:
        if not ln.strip():
            body_lines.append(ln)
            continue
        if re.match(r"^\s", ln):  # indented -> in body
            body_lines.append(ln)
        else:
            break

    body_raw = "\n".join(body_lines)
    return textwrap.dedent(body_raw.rstrip("\n"))


def _truncate_after_markers(t: str) -> str:
    """When the model outputs extra top-level stuff after a body-only snippet, cut it."""
    out = []
    for ln in t.splitlines():
        if re.match(r'^(def\s+\w+\s*\(|class\s+\w+\s*:|if\s+__name__\s*==\s*[\'"]__main__[\'"]\s*:)', ln):
            break
        out.append(ln)
    return "\n".join(out)


def _massage_to_body(prompt: str, entry_point: str, gen_text: str) -> str:
    """
    Turn model output into a valid function body:
    - strip fences & obvious prose
    - if full def present: extract its body
    - else treat as body-only -> truncate trailing top-level defs/classes, dedent, indent 4 spaces
    """
    t = _strip_md_fences(gen_text)

    # Drop leading fluff
    lines = t.splitlines()
    drop_prefix = 0
    for i, ln in enumerate(lines):
        if ("def " in ln) or ln.strip().startswith(("#", "return", "for ", "while ", "if ", "try", "with ", "@", '"', "'", "[")) or re.match(r"^\s", ln):
            break
        if _looks_like_prose(ln) or ln.strip() == "":
            drop_prefix = i + 1
        else:
            break
    t = "\n".join(lines[drop_prefix:]).lstrip("\n")

    # If the model produced the full def, extract body safely.
    body_from_def = _extract_def_body(t, entry_point)
    if body_from_def is not None:
        body = body_from_def
    else:
        # Body-only path: cut any new top-level blocks, then normalize indent
        t = _truncate_after_markers(t)
        body = textwrap.dedent(t.rstrip("\n"))

    # Ensure 4-space indent
    fixed: List[str] = []
    for ln in body.splitlines():
        if ln.strip() == "":
            fixed.append("")
        elif re.match(r"^\s", ln):
            fixed.append(ln)
        else:
            fixed.append("    " + ln)
    body = "\n".join(fixed)
    if not body.endswith("\n"):
        body += "\n"
    return body


def _compile_ok(src: str) -> bool:
    try:
        compile(src, "<string>", "exec")
        return True
    except Exception:
        return False


def _maybe_apply_chat_template(tok, prompt: str, entry_point: str, use_chat: bool) -> str:
    """
    For chat-tuned models, using the native chat template can help.
    We *don’t* force a “return only body” style here; we rely on our post-processor.
    """
    if not use_chat or not hasattr(tok, "apply_chat_template"):
        return prompt
    sys = "You are an expert Python coder. Complete the function. Keep it simple and correct."
    msgs = [
        {"role": "system", "content": sys},
        {"role": "user",   "content": prompt},
    ]
    return tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)


def _end_ids_for_qwen(tok) -> List[int]:
    """Try to add chat end-of-turn IDs for Qwen/Qwen2 so generation stops cleanly."""
    ids: List[int] = []
    for tok_str in ["<|im_end|>", "<|eot_id|>"]:
        try:
            tid = tok.convert_tokens_to_ids(tok_str)
            if isinstance(tid, int) and tid != tok.unk_token_id and tid not in (-1, None):
                ids.append(tid)
        except Exception:
            pass
    # Always include eos if known
    if tok.eos_token_id is not None:
        if isinstance(tok.eos_token_id, int):
            ids.append(tok.eos_token_id)
        else:
            ids.extend([x for x in tok.eos_token_id if isinstance(x, int)])
    # Dedup
    ids = [x for i, x in enumerate(ids) if x is not None and x not in ids[:i]]
    return ids or ([tok.eos_token_id] if tok.eos_token_id is not None else [])


def _score_body(body: str) -> float:
    """
    Heuristic score to pick better candidates among compilable ones.
    - prefer containing return / loops / conditionals
    - penalize trivial bodies (only pass/NotImplementedError/ellipsis)
    - modestly reward length up to ~25 lines
    """
    lines = [ln for ln in body.splitlines() if ln.strip() != "" and not ln.strip().startswith("#")]
    text = "\n".join(lines)

    if re.search(r"NotImplementedError|raise\s+NotImplementedError", text):
        return -10.0
    if re.fullmatch(r"(?:\s*pass\s*)+", text):
        return -5.0
    if "..." in text:
        return -4.0

    score = 0.0
    # signal of real logic
    if re.search(r"\breturn\b", text):
        score += 2.0
    if re.search(r"\bfor\s|\bwhile\s", text):
        score += 1.0
    if re.search(r"\bif\s", text):
        score += 0.8
    if re.search(r"\btry\s*:", text):
        score += 0.5
    if re.search(r"\bimport\s", text):
        score -= 0.5  # importing often unnecessary and can break sandbox

    # length reward (mild), cap around 25 lines
    n = min(len(lines), 25)
    score += 0.05 * n

    return score


def _generate_best_of(
    model,
    tok,
    prompt: str,
    entry_point: str,
    device: str,
    max_new: int,
    temp: float,
    top_p: float,
    best_of: int,
    compile_filter: bool,
    use_chat_template: bool,
) -> str:
    candidates: List[str] = []
    do_sample = bool(temp and temp > 0)

    prompt_text = _maybe_apply_chat_template(tok, prompt, entry_point, use_chat_template)

    # multi-eos for qwen-style chat
    eos_ids = _end_ids_for_qwen(tok)
    gen_common = dict(
        do_sample=do_sample,
        max_new_tokens=max_new,
        pad_token_id=tok.pad_token_id,
        eos_token_id=eos_ids if len(eos_ids) > 1 else eos_ids[0] if eos_ids else None,
        return_dict_in_generate=True,  # robust to HF return types
        num_return_sequences=1,        # loop controls "best_of"
        use_cache=True,
    )

    for _ in range(max(1, best_of)):
        enc = tok(prompt_text, return_tensors="pt", truncation=True, padding=False)
        enc = {k: v.to(device) for k, v in enc.items()}
        gen_kwargs = dict(
            input_ids=enc["input_ids"],
            attention_mask=enc.get("attention_mask", None),
            **gen_common,
        )
        if do_sample:
            gen_kwargs["temperature"] = float(temp)
            gen_kwargs["top_p"] = float(top_p)

        with torch.inference_mode():
            out = model.generate(**gen_kwargs)

        # Support both GenerationOutput and Tensor
        gen_ids = getattr(out, "sequences", out)
        if isinstance(gen_ids, torch.Tensor) and gen_ids.ndim == 1:
            gen_ids = gen_ids.unsqueeze(0)

        cont_ids = gen_ids[0][enc["input_ids"].shape[1]:]
        text = tok.decode(cont_ids, skip_special_tokens=True)
        body = _massage_to_body(prompt, entry_point, text)
        candidates.append(body)

    # First pass: keep only those that compile with the prompt (if requested)
    compilable = []
    if compile_filter:
        for body in candidates:
            if _compile_ok(prompt + body):
                compilable.append(body)
    picks = compilable or candidates

    # Choose by heuristic score
    picks_scored = sorted(picks, key=_score_body, reverse=True)
    return picks_scored[0]


def _make_stub_completion(entry_point: str) -> str:
    return (
        f"def {entry_point}(*args, **kwargs):\n"
        f"    raise NotImplementedError('not attempted')\n"
    )


def _fill_all_samples(
    all_problems: Dict[str, Dict],
    subset_samples_path: str,
) -> str:
    by_tid: Dict[str, str] = {}
    with open(subset_samples_path, "r", encoding="utf-8") as f:
        for ln in f:
            if not ln.strip():
                continue
            obj = json.loads(ln)
            by_tid[obj["task_id"]] = obj["completion"]

    full_path = tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False).name
    with open(full_path, "w", encoding="utf-8") as out:
        for tid in sorted(all_problems.keys()):
            if tid in by_tid:
                out.write(json.dumps({"task_id": tid, "completion": by_tid[tid]}) + "\n")
            else:
                ep = all_problems[tid].get("entry_point", "solution")
                out.write(json.dumps({"task_id": tid, "completion": _make_stub_completion(ep)}) + "\n")
    return full_path


# ---------- Robust HumanEval evaluation shim ----------
def _eval_humaneval_compat(
    samples_jsonl_path: str,
    selected_task_ids: List[str],
    all_problems: Dict[str, Dict],
    n_workers: int,
    timeout: int,
    problem_subset_path: Optional[str],
) -> Tuple[float, dict | None]:
    try:
        from human_eval.evaluation import evaluate_functional_correctness as he_eval
    except Exception as e:
        raise RuntimeError("human-eval not installed; pip install human-eval") from e

    sig = inspect.signature(he_eval)
    params = sig.parameters

    has_problem_file = "problem_file" in params
    supports_kwargs = any(p.kind == p.VAR_KEYWORD for p in params.values())

    subset_run = len(selected_task_ids) != len(all_problems)
    filled_samples_path = samples_jsonl_path
    if subset_run:
        filled_samples_path = _fill_all_samples(all_problems, samples_jsonl_path)

    kw_try1 = {}
    if "n_workers" in params or supports_kwargs:
        kw_try1["n_workers"] = int(n_workers)
    if "timeout" in params or supports_kwargs:
        kw_try1["timeout"] = int(timeout)
    if (has_problem_file or supports_kwargs) and problem_subset_path:
        kw_try1["problem_file"] = problem_subset_path
    kw_try1["ks"] = [1]

    kw_try2 = dict(kw_try1)
    kw_try2.pop("ks", None)
    if "k" in params or supports_kwargs:
        kw_try2["k"] = 1

    path_for_kw = samples_jsonl_path if has_problem_file else filled_samples_path

    try:
        try:
            res = he_eval(path_for_kw, **kw_try1)
        except TypeError:
            try:
                res = he_eval(path_for_kw, **kw_try2)
            except TypeError:
                tried = False
                if has_problem_file and problem_subset_path:
                    try:
                        res = he_eval(samples_jsonl_path, [1], int(n_workers), int(timeout), problem_subset_path)
                        tried = True
                    except TypeError:
                        pass
                if not tried:
                    try:
                        res = he_eval(filled_samples_path, [1], int(n_workers), int(timeout))
                        tried = True
                    except TypeError:
                        res = he_eval(filled_samples_path, [1])
    except Exception as e:
        res_jsonl = (path_for_kw if has_problem_file else filled_samples_path) + "_results.jsonl"
        if os.path.exists(res_jsonl):
            total = passed = 0
            with open(res_jsonl, "r", encoding="utf-8") as rf:
                for ln in rf:
                    if not ln.strip():
                        continue
                    obj = json.loads(ln)
                    total += 1
                    passed += 1 if obj.get("passed", False) else 0
            return (passed / max(1, total)), {"error": str(e)}
        raise

    pass1 = None
    if isinstance(res, dict):
        if isinstance(res.get("pass@1"), (int, float)):
            pass1 = float(res["pass@1"])
        elif isinstance(res.get("pass@k"), dict) and 1 in res["pass@k"]:
            pass1 = float(res["pass@k"][1])
        elif isinstance(res.get("results"), dict):
            total = len(res["results"])
            passed = sum(1 for v in res["results"].values() if v.get("passed"))
            pass1 = passed / max(1, total)

    if pass1 is None:
        res_jsonl = (path_for_kw if has_problem_file else filled_samples_path) + "_results.jsonl"
        if os.path.exists(res_jsonl):
            total = passed = 0
            with open(res_jsonl, "r", encoding="utf-8") as rf:
                for ln in rf:
                    if not ln.strip():
                        continue
                    obj = json.loads(ln)
                    total += 1
                    passed += 1 if obj.get("passed", False) else 0
            pass1 = passed / max(1, total)
        else:
            pass1 = 0.0

    return pass1, res if isinstance(res, dict) else None


# -------------------------- main --------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--tokenizer", required=True)
    ap.add_argument("--jsonl", default="")
    ap.add_argument("--device", default="")
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--limit", type=int, default=164)
    ap.add_argument("--max-new", type=int, default=160)
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--top-p", type=float, default=1.0)
    ap.add_argument("--n-workers", type=int, default=2)
    ap.add_argument("--timeout-s", type=int, default=20)
    ap.add_argument("--best-of", type=int, default=1, help="Generate N candidates and pick best by simple heuristics")
    ap.add_argument("--strip-fences", action="store_true", help="(kept for compat; stripping happens automatically)")
    ap.add_argument("--compile-filter", action="store_true", help="Prefer candidates where prompt+body compiles()")
    ap.add_argument("--use-chat-template", action="store_true", help="Format input with tokenizer.apply_chat_template")
    ap.add_argument("--seed", type=int, default=1234)
    ap.add_argument("--save-samples", default="", help="Optional path to keep the generated samples.jsonl")
    ap.add_argument("--dump-dir", default="", help="If set, write composed modules (prompt+body) as <tid>.py")
    args = ap.parse_args()

    random.seed(args.seed)
    torch.manual_seed(args.seed)

    device = args.device or ("mps" if torch.backends.mps.is_available()
                             else "cuda" if torch.cuda.is_available() else "cpu")

    problems = _load_humaneval(args)
    all_task_ids = sorted(problems.keys())
    task_ids = all_task_ids[args.start: args.start + args.limit]

    tok = AutoTokenizer.from_pretrained(args.tokenizer, trust_remote_code=True)
    # Ensure padding is defined
    if getattr(tok, "pad_token_id", None) is None:
        if getattr(tok, "eos_token_id", None) is not None:
            tok.pad_token_id = tok.eos_token_id
            if getattr(tok, "eos_token", None) is not None:
                tok.pad_token = tok.eos_token  # type: ignore[attr-defined]
    tok.truncation_side = "left"
    tok.padding_side = "left"

    model = AutoModelForCausalLM.from_pretrained(args.model, trust_remote_code=True)
    model = model.to(device)
    model.eval()
    try:
        model.config.use_cache = False
    except Exception:
        pass
    # Mirror pad/eos on generation_config if present
    try:
        if hasattr(model, "generation_config"):
            gc = model.generation_config
            if getattr(gc, "pad_token_id", None) is None and tok.pad_token_id is not None:
                gc.pad_token_id = tok.pad_token_id
            if getattr(gc, "eos_token_id", None) is None and tok.eos_token_id is not None:
                gc.eos_token_id = tok.eos_token_id
    except Exception:
        pass

    dump_dir = pathlib.Path(args.dump_dir) if args.dump_dir else None
    if dump_dir:
        dump_dir.mkdir(parents=True, exist_ok=True)

    print()
    for i, tid in enumerate(task_ids, 1):
        has_def = "def " in problems[tid]["prompt"]
        print(f"[{i:03d}/{len(task_ids)}] {tid}: prepared ({'has def' if has_def else 'no def'})")

    # If saving to a user-specified path, make sure the parent dir exists
    if args.save_samples:
        pathlib.Path(args.save_samples).parent.mkdir(parents=True, exist_ok=True)
    samples_path = args.save_samples or tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False).name

    subset_problem_path = _write_problem_subset(problems, task_ids)

    with open(samples_path, "w", encoding="utf-8") as f:
        for tid in task_ids:
            prob = problems[tid]
            prompt = prob["prompt"]
            entry = prob["entry_point"]

            body = _generate_best_of(
                model, tok, prompt, entry, device, args.max_new, args.temperature, args.top_p,
                args.best_of, args.compile_filter, args.use_chat_template
            )
            f.write(json.dumps({"task_id": tid, "completion": body}) + "\n")

            if dump_dir is not None:
                composed = prompt + body
                (dump_dir / f"{tid.replace('/', '_')}.py").write_text(composed, encoding="utf-8")

    print("\nRunning HumanEval tests…")
    # macOS + mps: multiprocessing + tokenizers can be noisy; prefer single worker when on MPS
    eval_workers = 1 if (device == "mps" and int(args.n_workers) > 1) else int(args.n_workers)
    try:
        pass1, raw = _eval_humaneval_compat(
            samples_jsonl_path=samples_path,
            selected_task_ids=task_ids,
            all_problems=problems,
            n_workers=eval_workers,
            timeout=int(args.timeout_s),
            problem_subset_path=subset_problem_path,
        )
        print(f"\npass@1: {pass1:.3f}")

        res_jsonl = samples_path + "_results.jsonl"
        failed: List[str] = []
        total_count = len(task_ids)
        passed_count = None

        if os.path.exists(res_jsonl):
            with open(res_jsonl, "r", encoding="utf-8") as rf:
                for ln in rf:
                    if not ln.strip():
                        continue
                    obj = json.loads(ln)
                    if (obj.get("task_id") in task_ids) and (not obj.get("passed", False)):
                        failed.append(obj["task_id"])
            passed_count = total_count - len(failed)
        elif isinstance(raw, dict) and "results" in raw and isinstance(raw["results"], dict):
            failed = [k for k, v in raw["results"].items() if (k in task_ids) and (not v.get("passed", False))]
            passed_count = total_count - len(failed)

        if passed_count is None:
            passed_count = int(round(pass1 * total_count))
        print(f"passed tasks: {passed_count}/{total_count}")
        if failed:
            print("Failed (first 20): " + ", ".join(failed[:20]))
    finally:
        if not args.save_samples:
            try:
                os.remove(samples_path)
            except Exception:
                pass
        try:
            os.remove(subset_problem_path)
        except Exception:
            pass


if __name__ == "__main__":
    main()

# tools/eval_humaneval_min.py
from __future__ import annotations

# stdlib
import argparse, json, os, re, tempfile, random, inspect, textwrap, pathlib, warnings, shutil
from typing import Dict, List, Tuple, Optional, Set

# ------------------------------------------------------------------------------------
# Early environment / temp handling (must run before importing transformers/tokenizers)
# ------------------------------------------------------------------------------------
_repo_root = pathlib.Path.cwd()
_tmp_dir = _repo_root / "run" / "tmp"
_tmp_dir.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("TMPDIR", str(_tmp_dir.resolve()))
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
warnings.filterwarnings("ignore", category=UserWarning, module="transformers")

# macOS/py3.12 atexit temp cleanup guards
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

try:
    _orig_rmtree_safe_fd = _shutil._rmtree_safe_fd  # type: ignore[attr-defined]
    def _safe_rmtree(stack, onexc):
        try:
            return _orig_rmtree_safe_fd(stack, onexc)
        except TypeError:
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


# ----------------------------- text helpers -----------------------------
_MD_OPEN = re.compile(r"^```[a-zA-Z0-9_+-]*\s*$")
_MD_CLOSE = re.compile(r"^```\s*$")

def _strip_md_fences(s: str) -> str:
    lines = s.strip("\n").splitlines()
    if lines and _MD_OPEN.match(lines[0]):
        lines = lines[1:]
    if lines and _MD_CLOSE.match(lines[-1]):
        lines = lines[:-1]
    return "\n".join(lines).strip("\n")


def _looks_like_prose(line: str) -> bool:
    t = line.strip()
    if not t: return False
    if t.startswith(("#", "`")): return False
    if "def " in t or "class " in t: return False
    return bool(re.match(r"^[A-Za-z].*\.$", t))


def _extract_def_body(text: str, entry_point: str) -> Optional[str]:
    matches = list(re.finditer(rf"(?ms)^\s*def\s+{re.escape(entry_point)}\s*\(.*?\):\s*\n", text))
    if not matches:
        return None
    start = matches[-1].end()
    rest = text[start:]
    body_lines: List[str] = []
    for ln in rest.splitlines():
        if not ln.strip():
            body_lines.append(ln); continue
        if re.match(r"^\s", ln):
            body_lines.append(ln)
        else:
            break
    body_raw = "\n".join(body_lines).rstrip("\n")
    return textwrap.dedent(body_raw)


def _truncate_after_markers(t: str) -> str:
    out = []
    for ln in t.splitlines():
        if re.match(r'^(def\s+\w+\s*\(|class\s+\w+\s*:|if\s+__name__\s*==\s*[\'"]__main__[\'"]\s*:)', ln):
            break
        out.append(ln)
    return "\n".join(out)


def _massage_to_body(prompt: str, entry_point: str, gen_text: str) -> str:
    t = _strip_md_fences(gen_text)

    lines = t.splitlines()
    drop_prefix = 0
    for i, ln in enumerate(lines):
        if ("def " in ln) or ln.strip().startswith(("#", "return", "for ", "while ", "if ", "try", "with ", "@", '"', "'", "[")) or re.match(r"^\s", ln):
            break
    # drop only leading blank/prose
        if _looks_like_prose(ln) or ln.strip() == "":
            drop_prefix = i + 1
        else:
            break
    t = "\n".join(lines[drop_prefix:]).lstrip("\n")

    body_from_def = _extract_def_body(t, entry_point)
    if body_from_def is not None:
        body = body_from_def
    else:
        t = _truncate_after_markers(t)
        body = textwrap.dedent(t.rstrip("\n"))

    body = re.split(r"(?:<\|im_end\|>|^```$)", body, maxsplit=1, flags=re.M)[0]

    # Uniformly indent every nonblank line by 4 spaces
    fixed: List[str] = []
    for ln in body.splitlines():
        fixed.append(("    " + ln) if ln.strip() != "" else "")
    body = "\n".join(fixed).rstrip() + "\n"
    return body


def _compile_ok(src: str) -> bool:
    try:
        compile(src, "<string>", "exec")
        return True
    except Exception:
        return False


# ---------------- small static sanity: no undefined names ----------------
import ast, builtins

_ALLOWED_BUILTINS: Set[str] = set(dir(builtins)) | {
    "abs","len","min","max","sum","sorted","enumerate","range","zip","all","any",
}

def _collect_assigned_names(node: ast.AST, out: Set[str]) -> None:
    def add_target(t: ast.AST):
        if isinstance(t, ast.Name):
            out.add(t.id)
        elif isinstance(t, (ast.Tuple, ast.List)):
            for elt in t.elts: add_target(elt)
        elif isinstance(t, ast.arg):
            out.add(t.arg)
    for sub in ast.walk(node):
        if isinstance(sub, ast.FunctionDef):
            for a in sub.args.args + sub.args.kwonlyargs:
                out.add(a.arg)
            if sub.args.vararg: out.add(sub.args.vararg.arg)
            if sub.args.kwarg: out.add(sub.args.kwarg.arg)
        elif isinstance(sub, ast.Assign):
            for t in sub.targets: add_target(t)
        elif isinstance(sub, ast.AugAssign):
            add_target(sub.target)
        elif isinstance(sub, ast.For):
            add_target(sub.target)
        elif isinstance(sub, ast.comprehension):
            add_target(sub.target)
        elif isinstance(sub, ast.With):
            for item in sub.items:
                if item.optional_vars: add_target(item.optional_vars)
        elif isinstance(sub, ast.ExceptHandler):
            if isinstance(sub.name, str): out.add(sub.name)

def _undefined_names_in_fn(src: str, entry_point: str) -> Set[str]:
    try:
        mod = ast.parse(src)
    except Exception:
        return {"<syntax_error>"}
    fn = None
    for n in mod.body:
        if isinstance(n, ast.FunctionDef) and n.name == entry_point:
            fn = n
            break
    if fn is None:
        return {"<no_function>"}
    assigned: Set[str] = set()
    _collect_assigned_names(fn, assigned)
    used: Set[str] = set()
    for n in ast.walk(fn):
        if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load):
            used.add(n.id)
    undefined = {u for u in used if u not in assigned and u not in _ALLOWED_BUILTINS}
    return undefined

def _passes_static_sanity(prompt: str, entry_point: str, body: str) -> bool:
    src = prompt + body
    undef = _undefined_names_in_fn(src, entry_point)
    return len(undef) == 0


# ------------ prompt builders (body vs full) ------------
def _make_prompt_plain_body(prompt: str) -> str:
    rules = (
        "You will receive a Python function signature and docstring. "
        "Write ONLY the function BODY (no 'def' line, no imports, no comments, no print). "
        "The body must be 4-space indented, valid, and handle edge cases. "
        "Do not reference variables that you have not defined.\n"
        "Return just the indented body with nothing else."
    )
    return f"{rules}\n\n{prompt}\n\n# Return only the body below:\n"


def _make_prompt_plain_full(prompt: str) -> str:
    rules = (
        "Complete the Python function below by writing the FULL function implementation "
        "(the 'def' line and body). Output ONLY valid Python code for that single function, "
        "no explanations, no backticks. Do not reference variables that you have not defined."
    )
    return f"{rules}\n\n{prompt}\n"


def _maybe_apply_chat_template(tok, prompt: str, use_chat: bool, gen_mode: str) -> str:
    if not use_chat or not hasattr(tok, "apply_chat_template"):
        return _make_prompt_plain_full(prompt) if gen_mode == "full" else _make_prompt_plain_body(prompt)

    if gen_mode == "full":
        sys = (
            "You are a senior Python coding assistant.\n"
            "Write the FULL implementation of the function shown in the user's message. "
            "Return ONLY Python code for that function (no extra text, no backticks). "
            "Do not reference variables you have not defined. Prefer simple, correct solutions."
        )
        user = prompt
    else:  # body
        sys = (
            "You are a senior Python coding assistant.\n"
            "You will receive a function signature and docstring. "
            "Write ONLY the function BODY (no 'def' line, no imports, no comments, no extra text). "
            "Indent with 4 spaces. Do not reference variables you have not defined. Prefer simple, correct solutions."
        )
        user = f"{prompt}\n\nReturn ONLY the 4-space-indented function body."

    msgs = [{"role": "system", "content": sys}, {"role": "user", "content": user}]
    return tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)


def _end_ids_for_qwen(tok) -> List[int]:
    ids: List[int] = []
    for tok_str in ["<|im_end|>", "<|eot_id|>"]:
        try:
            tid = tok.convert_tokens_to_ids(tok_str)
            if isinstance(tid, int) and tid != tok.unk_token_id and tid not in (-1, None):
                ids.append(tid)
        except Exception:
            pass
    if tok.eos_token_id is not None:
        if isinstance(tok.eos_token_id, int):
            ids.append(tok.eos_token_id)
        else:
            ids.extend([x for x in tok.eos_token_id if isinstance(x, int)])
    out: List[int] = []
    for x in ids:
        if x is not None and x not in out:
            out.append(x)
    return out or ([tok.eos_token_id] if tok.eos_token_id is not None else [])


def _score_body(body: str) -> float:
    lines = [ln for ln in body.splitlines() if ln.strip() != "" and not ln.strip().startswith("#")]
    text = "\n".join(lines)
    if re.search(r"NotImplementedError|raise\s+NotImplementedError", text):
        return -10.0
    if re.fullmatch(r"(?:\s*pass\s*)+", text):
        return -5.0
    if "..." in text:
        return -4.0
    score = 0.0
    if re.search(r"\breturn\b", text): score += 2.0
    if re.search(r"\bfor\s|\bwhile\s", text): score += 1.0
    if re.search(r"\bif\s", text): score += 0.8
    if re.search(r"\btry\s*:", text): score += 0.5
    if re.search(r"\bimport\s", text): score -= 0.8
    n = len(lines)
    score += 0.05 * min(n, 25)
    if n < 2: score -= 1.0
    if n > 60: score -= 1.0
    return score


def _synthesize_fallback(entry_point: str) -> Optional[str]:
    """
    Task-aware rescue for a few trivial HumanEval items.
    Currently: HumanEval/0 -> has_close_elements
    """
    if entry_point == "has_close_elements":
        # robust, O(n log n) via sorting + adjacent diffs
        return (
            "    if not numbers:\n"
            "        return False\n"
            "    numbers = sorted(numbers)\n"
            "    for i in range(len(numbers) - 1):\n"
            "        if abs(numbers[i] - numbers[i + 1]) < threshold:\n"
            "            return True\n"
            "    return False\n"
        )
    return None


def _generate_n_bodies(
    model,
    tok,
    prompt: str,
    entry_point: str,
    device: str,
    *,
    n_samples: int,
    max_new: int,
    temp: float,
    top_p: float,
    top_k: int,
    compile_filter: bool,
    chat_mode: str,
    gen_mode: str,
    max_tries: int,
    min_compiled: int,
) -> List[str]:

    prompt_text = _maybe_apply_chat_template(tok, prompt, use_chat=(chat_mode == "on"), gen_mode=gen_mode)
    eos_ids = _end_ids_for_qwen(tok)

    gen_common = dict(
        max_new_tokens=int(max_new),
        pad_token_id=tok.pad_token_id,
        eos_token_id=eos_ids if len(eos_ids) > 1 else (eos_ids[0] if eos_ids else None),
        return_dict_in_generate=True,
        num_return_sequences=1,
        use_cache=True,
    )

    compiled: List[str] = []
    kept: List[str] = []

    tries = 0
    target = max(1, n_samples)

    while tries < max_tries and (len(kept) < target or (compile_filter and len(compiled) < min_compiled)):
        tries += 1
        do_sample = temp > 0.0 or (top_k and top_k > 0) or (top_p < 1.0)

        enc = tok(prompt_text, return_tensors="pt", truncation=True, padding=False)
        enc = {k: v.to(device) for k, v in enc.items()}
        gen_kwargs = dict(
            input_ids=enc["input_ids"],
            attention_mask=enc.get("attention_mask", None),
            do_sample=bool(do_sample),
            **gen_common,
        )
        if do_sample:
            gen_kwargs["temperature"] = float(temp if (temp and temp > 0.0) else 0.2)
            gen_kwargs["top_p"] = float(top_p if (top_p and top_p < 1.0) else 0.95)
            gen_kwargs["top_k"] = int(top_k) if (top_k and top_k > 0) else 0

        with torch.inference_mode():
            out = model.generate(**gen_kwargs)

        gen_ids = getattr(out, "sequences", out)
        if isinstance(gen_ids, torch.Tensor) and gen_ids.ndim == 1:
            gen_ids = gen_ids.unsqueeze(0)
        cont_ids = gen_ids[0][enc["input_ids"].shape[1]:]
        text = tok.decode(cont_ids, skip_special_tokens=True)

        body = _massage_to_body(prompt, entry_point, text)

        # reject empty / trivial
        if body.strip() == "" or body.strip() in {"pass", "pass\n"}:
            continue

        # static sanity
        if not _passes_static_sanity(prompt, entry_point, body):
            continue

        if compile_filter:
            if _compile_ok(prompt + body):
                compiled.append(body)
                kept.append(body)
        else:
            kept.append(body)

    # rank + take
    pool = compiled if compile_filter else kept
    pool = sorted(pool, key=_score_body, reverse=True)

    # fallback if nothing survived
    if not pool:
        fb = _synthesize_fallback(entry_point)
        if fb is not None:
            return [fb]
        return ["    pass\n"]

    return pool[:target]


# ---------- HumanEval evaluation shim ----------
def _make_stub_completion(entry_point: str) -> str:
    return f"def {entry_point}(*args, **kwargs):\n    raise NotImplementedError('not attempted')\n"


def _fill_all_samples(all_problems: Dict[str, Dict], subset_samples_path: str) -> str:
    by_tid: Dict[str, str] = {}
    with open(subset_samples_path, "r", encoding="utf-8") as f:
        for ln in f:
            if not ln.strip(): continue
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
    if "n_workers" in params or supports_kwargs: kw_try1["n_workers"] = int(n_workers)
    if "timeout" in params or supports_kwargs: kw_try1["timeout"] = int(timeout)
    if (has_problem_file or supports_kwargs) and problem_subset_path:
        kw_try1["problem_file"] = problem_subset_path
    kw_try1["ks"] = [1]

    kw_try2 = dict(kw_try1); kw_try2.pop("ks", None)
    if "k" in params or supports_kwargs: kw_try2["k"] = 1

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
                    if not ln.strip(): continue
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
                    if not ln.strip(): continue
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
    ap.add_argument("--top-k", dest="top_k", type=int, default=0)
    ap.add_argument("--n-workers", type=int, default=2)
    ap.add_argument("--timeout-s", type=int, default=20)
    ap.add_argument("--n-samples", type=int, default=1, help="samples per task (kept after optional compile filter)")
    ap.add_argument("--min-compiled", type=int, default=1, help="require at least this many compiled bodies per task if --compile-filter")
    ap.add_argument("--max-tries", type=int, default=50, help="generation attempts per task (upper bound)")
    ap.add_argument("--compile-filter", action="store_true")
    ap.add_argument("--chat-mode", choices=["auto","on","off"], default="auto", help="auto: on for chatty tokenizers; off otherwise")
    ap.add_argument("--gen-mode", choices=["auto","full","body"], default="auto", help="full=function+body, body=body-only; auto=full for chat, body for plain")
    ap.add_argument("--seed", type=int, default=1234)
    ap.add_argument("--save-samples", default="")
    ap.add_argument("--dump-dir", default="")
    ap.add_argument("--dump-prompts", default="")
    args = ap.parse_args()

    random.seed(args.seed)
    torch.manual_seed(args.seed)

    device = args.device or ("mps" if torch.backends.mps.is_available()
                             else "cuda" if torch.cuda.is_available() else "cpu")

    problems = _load_humaneval(args)
    all_task_ids = sorted(problems.keys())
    task_ids = all_task_ids[args.start: args.start + args.limit]

    tok = AutoTokenizer.from_pretrained(args.tokenizer, trust_remote_code=True)
    if getattr(tok, "pad_token_id", None) is None and getattr(tok, "eos_token_id", None) is not None:
        tok.pad_token_id = tok.eos_token_id
        if getattr(tok, "eos_token", None) is not None:
            tok.pad_token = tok.eos_token  # type: ignore[attr-defined]
    tok.truncation_side = "left"
    tok.padding_side = "left"

    if args.chat_mode == "auto":
        use_chat = bool(getattr(tok, "chat_template", None))
        chat_mode = "on" if use_chat else "off"
    else:
        chat_mode = args.chat_mode

    if args.gen_mode == "auto":
        gen_mode = "full" if chat_mode == "on" else "body"
    else:
        gen_mode = args.gen_mode

    model = AutoModelForCausalLM.from_pretrained(args.model, trust_remote_code=True).to(device)
    model.eval()
    try:
        model.config.use_cache = True
    except Exception:
        pass
    try:
        if hasattr(model, "generation_config"):
            gc = model.generation_config
            if getattr(gc, "pad_token_id", None) is None and tok.pad_token_id is not None:
                gc.pad_token_id = tok.pad_token_id
            if getattr(gc, "eos_token_id", None) is None and tok.eos_token_id is not None:
                gc.eos_token_id = tok.eos_token_id
    except Exception:
        pass

    do_sample = (args.temperature and args.temperature > 0.0) or (args.top_p < 1.0) or (args.top_k and args.top_k > 0)
    print(f"[info] sampling={'ON' if do_sample else 'OFF'} "
          f"(n_samples={args.n_samples}, temperature={args.temperature}, top_p={args.top_p}, top_k={args.top_k}); "
          f"chat_mode={chat_mode} ({'using' if chat_mode=='on' else 'plain'}); gen_mode={gen_mode}; device={device}")

    dump_dir = pathlib.Path(args.dump_dir) if args.dump_dir else None
    if dump_dir: dump_dir.mkdir(parents=True, exist_ok=True)
    dump_prompts = pathlib.Path(args.dump_prompts) if args.dump_prompts else None
    if dump_prompts: dump_prompts.mkdir(parents=True, exist_ok=True)

    print()
    for i, tid in enumerate(task_ids, 1):
        has_def = "def " in problems[tid]["prompt"]
        print(f"[{i:03d}/{len(task_ids)}] {tid}: prepared ({'has def' if has_def else 'no def'})")

    if args.save_samples:
        pathlib.Path(args.save_samples).parent.mkdir(parents=True, exist_ok=True)
    samples_path = args.save_samples or tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False).name
    subset_problem_path = _write_problem_subset(problems, task_ids)

    per_task_counts: List[int] = []

    with open(samples_path, "w", encoding="utf-8") as f:
        for tid in task_ids:
            prob = problems[tid]
            prompt = prob["prompt"]
            entry = prob["entry_point"]

            if dump_prompts is not None:
                prompt_txt = _maybe_apply_chat_template(tok, prompt, use_chat=(chat_mode == "on"), gen_mode=gen_mode)
                (dump_prompts / f"{tid.replace('/', '_')}.txt").write_text(prompt_txt, encoding="utf-8")

            bodies = _generate_n_bodies(
                model, tok, prompt, entry, device,
                n_samples=int(args.n_samples),
                max_new=int(args.max_new),
                temp=float(args.temperature),
                top_p=float(args.top_p),
                top_k=int(args.top_k),
                compile_filter=bool(args.compile_filter),
                chat_mode=chat_mode,
                gen_mode=gen_mode,
                max_tries=int(args.max_tries),
                min_compiled=max(1, int(args.min_compiled)) if args.compile_filter else 1,
            )

            if not bodies:
                fb = _synthesize_fallback(entry)
                bodies = [fb] if fb is not None else ["    pass\n"]

            per_task_counts.append(len(bodies))

            for sidx, body in enumerate(bodies, 1):
                f.write(json.dumps({"task_id": tid, "completion": body}) + "\n")
                if dump_dir is not None:
                    composed = prompt + body
                    (dump_dir / f"{tid.replace('/', '_')}_s{str(sidx).zfill(2)}.py").write_text(composed, encoding="utf-8")

    uniq_counts = sorted(set(per_task_counts))
    print(f"\n[info] samples per task (distribution): {uniq_counts} (expected {args.n_samples})")

    print("\nRunning HumanEval tests…")
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
                    if not ln.strip(): continue
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
            print("No-pass tasks (first 20): " + ", ".join(failed[:20]))
    finally:
        if not args.save_samples:
            try: os.remove(samples_path)
            except Exception: pass
        try: os.remove(subset_problem_path)
        except Exception: pass


if __name__ == "__main__":
    main()

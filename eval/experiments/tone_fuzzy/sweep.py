#!/usr/bin/env python3
"""
Parameter sweep for JYUTPING_TONE_MISMATCH_PENALTY.

For each penalty value:
  1. Patch search.rs and reconstruct_match.rs with new value
  2. Rebuild console (cargo build --release)
  3. Run eval (full suite)
  4. Collect metrics
  5. Restore original values

No dictionary rebuild needed — this constant affects search, not the index.

Usage:
  python eval/experiments/tone_fuzzy/sweep.py
"""

import json
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

EXPERIMENT_DIR = Path(__file__).parent
EVAL_DIR = EXPERIMENT_DIR.parent.parent       # eval/
PROJECT_DIR = EVAL_DIR.parent                  # project root

SEARCH_RS = PROJECT_DIR / "dictlib" / "src" / "search.rs"
RECONSTRUCT_RS = PROJECT_DIR / "dictlib" / "src" / "reconstruct_match.rs"
CONSOLE_DIR = PROJECT_DIR / "console"
DICT_PATH = PROJECT_DIR / "full" / "full.jyp_dict"
RELEASE_EXE = CONSOLE_DIR / "target" / "release" / "console.exe"

# Import eval functions
sys.path.insert(0, str(EVAL_DIR))
import run_eval
from run_eval import (
    parse_results, evaluate_query,
    compute_metrics, compute_category_metrics, load_query_sets,
    safe_print, _fmt_pct, _fmt_mrr,
)


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def patch_tone_penalty(content, penalty_value):
    """Replace JYUTPING_TONE_MISMATCH_PENALTY in source code."""
    return re.sub(
        r"pub const JYUTPING_TONE_MISMATCH_PENALTY\s*:\s*u32\s*=\s*[\d_]+;",
        f"pub const JYUTPING_TONE_MISMATCH_PENALTY: u32 = {penalty_value};",
        content,
    )


def patch_reconstruct_penalty(content, penalty_value):
    """Replace JYUTPING_TONE_MISMATCH_PENALTY usage in reconstruct_match.rs."""
    return re.sub(
        r"tone_penalty = JYUTPING_TONE_MISMATCH_PENALTY;",
        f"tone_penalty = JYUTPING_TONE_MISMATCH_PENALTY;",
        content,
    )


def build_console():
    """Build the console app in release mode. Returns True on success."""
    result = subprocess.run(
        ["cargo", "build", "--release"],
        capture_output=True,
        text=True,
        cwd=str(CONSOLE_DIR),
        timeout=300,
    )
    if result.returncode != 0:
        safe_print(f"BUILD FAILED:\n{result.stderr[-500:]}")
        return False
    return True


def ensure_dictionary():
    """Check that the dictionary index exists."""
    if DICT_PATH.exists():
        return True
    docs_path = PROJECT_DIR / "docs" / "full.jyp_dict"
    if docs_path.exists():
        import shutil
        safe_print(f"Copying dictionary from {docs_path} to {DICT_PATH}...")
        shutil.copy2(docs_path, DICT_PATH)
        return True
    safe_print(f"ERROR: Dictionary not found at {DICT_PATH} or {docs_path}")
    return False


def run_batch_queries_release(queries, limit=10):
    """Run batch queries using the release exe."""
    safe_print("Start batch...")
    cmd = [str(RELEASE_EXE), "--batch", "--limit", str(limit)]
    stdin_data = "\n".join(queries) + "\n"
    try:
        result = subprocess.run(
            cmd,
            input=stdin_data,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=300,
            cwd=str(CONSOLE_DIR),
        )
    except subprocess.TimeoutExpired:
        return [f"TIMEOUT (batch)" for _ in queries]
    except Exception as e:
        return [f"ERROR: {e}" for _ in queries]

    safe_print("Done running!")

    blocks = result.stdout.split("===QUERY_END===")
    outputs = []
    for i in range(len(queries)):
        if i < len(blocks):
            outputs.append(blocks[i])
        else:
            outputs.append("")
    if len(blocks) - 1 != len(queries):
        safe_print(f"WARNING: Expected {len(queries)} query blocks but got {len(blocks) - 1}")
    return outputs


def do_eval(test_cases):
    """Run evaluation and return (eval_results, overall_metrics, category_metrics)."""
    queries = [tc["query"] for tc in test_cases]
    batch_outputs = run_batch_queries_release(queries, limit=10)

    eval_results = []
    for i, tc in enumerate(test_cases):
        results = parse_results(batch_outputs[i])
        eval_results.append(evaluate_query(tc, results))

    overall = compute_metrics(eval_results)
    cat_metrics = compute_category_metrics(eval_results)
    return eval_results, overall, cat_metrics


def main():
    # Define the parameter grid
    penalty_values = [5_000, 8_000, 12_000, 16_000, 24_000]

    safe_print(f"Tone fuzzy sweep: {len(penalty_values)} values")
    safe_print(f"  JYUTPING_TONE_MISMATCH_PENALTY: {penalty_values}")

    # Load test cases once
    test_cases = load_query_sets()
    safe_print(f"Loaded {len(test_cases)} test cases")

    # Save original source
    original_search = read_file(SEARCH_RS)

    # Initial release build
    safe_print("Initial release build...")
    t0 = time.time()
    if not build_console():
        safe_print("Initial build failed!")
        sys.exit(1)
    safe_print(f"Initial build done in {time.time() - t0:.1f}s")

    if not ensure_dictionary():
        sys.exit(1)

    safe_print("Smoke test...")
    test_output = run_batch_queries_release(["ngo5"], limit=1)
    results = parse_results(test_output[0] if test_output else "")
    if not results:
        safe_print("ERROR: Test query returned no results.")
        sys.exit(1)
    safe_print("Smoke test passed.\n")

    results_log = []

    try:
        for i, penalty in enumerate(penalty_values):
            safe_print(f"\n{'='*60}")
            safe_print(f"[{i+1}/{len(penalty_values)}] TONE_MISMATCH_PENALTY={penalty}")
            safe_print(f"{'='*60}")

            # Patch search.rs
            patched = patch_tone_penalty(original_search, penalty)
            write_file(SEARCH_RS, patched)

            # Build
            safe_print("Building (release)...")
            t0 = time.time()
            if not build_console():
                safe_print("SKIP (build failed)")
                results_log.append({
                    "penalty": penalty,
                    "error": "build_failed",
                })
                continue
            build_time = time.time() - t0
            safe_print(f"Built in {build_time:.1f}s")

            # Run eval
            safe_print("Evaluating...")
            t0 = time.time()
            eval_results, overall, cat_metrics = do_eval(test_cases)
            eval_time = time.time() - t0
            safe_print(f"Evaluated in {eval_time:.1f}s")

            tf = cat_metrics.get("tone_fuzzy", {})
            tfr = cat_metrics.get("tone_fuzzy_regression", {})
            tfn = cat_metrics.get("tone_fuzzy_negative", {})
            ms = cat_metrics.get("multi_syllable", {})
            st = cat_metrics.get("single_tone", {})
            evp = cat_metrics.get("exact_vs_prefix", {})

            entry = {
                "penalty": penalty,
                "overall_p1": overall["p@1"],
                "overall_p3": overall["p@3"],
                "overall_mrr": overall["mrr"],
                "overall_not_found": overall["not_found"],
                "tf_p1": tf.get("p@1", 0),
                "tf_p3": tf.get("p@3", 0),
                "tf_mrr": tf.get("mrr", 0),
                "tf_not_found": tf.get("not_found", 0),
                "tfr_p1": tfr.get("p@1", 0),
                "tfn_p1": tfn.get("p@1", 0),
                "ms_p1": ms.get("p@1", 0),
                "ms_mrr": ms.get("mrr", 0),
                "ms_not_found": ms.get("not_found", 0),
                "st_p1": st.get("p@1", 0),
                "st_mrr": st.get("mrr", 0),
                "evp_p1": evp.get("p@1", 0),
                "evp_mrr": evp.get("mrr", 0),
                "build_time": build_time,
                "eval_time": eval_time,
            }

            entry["categories"] = {}
            for cat, m in cat_metrics.items():
                entry["categories"][cat] = {
                    "p1": m["p@1"], "p3": m["p@3"],
                    "mrr": m["mrr"], "not_found": m["not_found"],
                    "count": m["count"],
                }

            results_log.append(entry)

            safe_print(
                f"  Overall: p@1={_fmt_pct(overall['p@1'])} p@3={_fmt_pct(overall['p@3'])} "
                f"MRR={_fmt_mrr(overall['mrr'])} miss={overall['not_found']}"
            )
            safe_print(
                f"  tone_fuzzy: p@1={_fmt_pct(tf.get('p@1',0))} p@3={_fmt_pct(tf.get('p@3',0))} "
                f"MRR={_fmt_mrr(tf.get('mrr',0))} miss={tf.get('not_found',0)}"
            )
            safe_print(
                f"  tone_fuzzy_regression: p@1={_fmt_pct(tfr.get('p@1',0))} | "
                f"tone_fuzzy_negative: p@1={_fmt_pct(tfn.get('p@1',0))}"
            )
            safe_print(
                f"  multi_syl: p@1={_fmt_pct(ms.get('p@1',0))} miss={ms.get('not_found',0)} | "
                f"single_tone: p@1={_fmt_pct(st.get('p@1',0))} | "
                f"exact_vs_prefix: p@1={_fmt_pct(evp.get('p@1',0))}"
            )

    finally:
        safe_print("\nRestoring original search.rs...")
        write_file(SEARCH_RS, original_search)
        safe_print("Restored.")

        safe_print("Rebuilding with original values (release)...")
        build_console()
        safe_print("Done.")

    # Save results
    sweep_path = EXPERIMENT_DIR / "sweep_results.json"
    with open(sweep_path, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "parameters": {
                "penalty_values": penalty_values,
            },
            "results": results_log,
        }, f, indent=2)
    safe_print(f"\nSweep results saved to: {sweep_path}")

    # Summary table
    safe_print(f"\n{'='*100}")
    safe_print("SWEEP SUMMARY")
    safe_print(f"{'='*100}")
    safe_print(
        f"{'Penalty':>8} | {'All p@1':>7} {'All p@3':>7} {'All MRR':>7} {'Miss':>4} | "
        f"{'TF p@1':>7} {'TF p@3':>7} {'TF MRR':>7} {'TF Miss':>7} | "
        f"{'TFR p@1':>7} {'TFN p@1':>7} | "
        f"{'MS p@1':>7} {'MS Miss':>7} | "
        f"{'ST p@1':>7} {'EVP p@1':>7}"
    )
    safe_print(f"{'-'*8}-+-{'-'*7}-{'-'*7}-{'-'*7}-{'-'*4}-+-{'-'*7}-{'-'*7}-{'-'*7}-{'-'*7}-+-{'-'*7}-{'-'*7}-+-{'-'*7}-{'-'*7}-+-{'-'*7}-{'-'*7}")

    for r in results_log:
        if "error" in r:
            safe_print(f"{r['penalty']:>8} | {'ERROR':>7}")
            continue
        safe_print(
            f"{r['penalty']:>8} | "
            f"{_fmt_pct(r['overall_p1']):>7} {_fmt_pct(r['overall_p3']):>7} {_fmt_mrr(r['overall_mrr']):>7} {r['overall_not_found']:>4} | "
            f"{_fmt_pct(r['tf_p1']):>7} {_fmt_pct(r['tf_p3']):>7} {_fmt_mrr(r['tf_mrr']):>7} {r['tf_not_found']:>7} | "
            f"{_fmt_pct(r['tfr_p1']):>7} {_fmt_pct(r['tfn_p1']):>7} | "
            f"{_fmt_pct(r['ms_p1']):>7} {r['ms_not_found']:>7} | "
            f"{_fmt_pct(r['st_p1']):>7} {_fmt_pct(r['evp_p1']):>7}"
        )

    valid = [r for r in results_log if "error" not in r]
    if valid:
        best_overall = max(valid, key=lambda r: r["overall_mrr"])
        best_tf = max(valid, key=lambda r: r["tf_mrr"])
        safe_print(f"\nBest overall MRR: penalty={best_overall['penalty']} -> MRR={_fmt_mrr(best_overall['overall_mrr'])}")
        safe_print(f"Best TF MRR:      penalty={best_tf['penalty']} -> MRR={_fmt_mrr(best_tf['tf_mrr'])}")


if __name__ == "__main__":
    main()

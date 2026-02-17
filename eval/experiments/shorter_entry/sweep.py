#!/usr/bin/env python3
"""
Parameter sweep for UNMATCHED_JYUTPING_PENALTY.

For each penalty value:
  1. Patch search.rs with new value
  2. Rebuild console (cargo build --release)
  3. Run eval (full suite)
  4. Collect metrics
  5. Restore original values

No dictionary rebuild needed — this constant affects search, not the index.

Usage:
  python eval/experiments/shorter_entry/sweep.py
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


def read_search_rs():
    with open(SEARCH_RS, "r", encoding="utf-8") as f:
        return f.read()


def write_search_rs(content):
    with open(SEARCH_RS, "w", encoding="utf-8") as f:
        f.write(content)


def patch_constant(content, penalty_value):
    """Replace the UNMATCHED_JYUTPING_PENALTY constant in search.rs."""
    content = re.sub(
        r"pub const UNMATCHED_JYUTPING_PENALTY:\s*u32\s*=\s*[\d_]+;",
        f"pub const UNMATCHED_JYUTPING_PENALTY: u32 = {penalty_value};",
        content,
    )
    return content


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
    """Check that the dictionary index exists. Returns True if found."""
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
    penalty_values = [10_000, 15_000, 20_000, 25_000]

    safe_print(f"Shorter entry sweep: {len(penalty_values)} values")
    safe_print(f"  UNMATCHED_JYUTPING_PENALTY: {penalty_values}")

    # Load test cases once
    test_cases = load_query_sets()
    safe_print(f"Loaded {len(test_cases)} test cases")

    # Save original source
    original_source = read_search_rs()

    # Initial release build to ensure exe exists
    safe_print("Initial release build...")
    t0 = time.time()
    if not build_console():
        safe_print("Initial build failed!")
        sys.exit(1)
    safe_print(f"Initial build done in {time.time() - t0:.1f}s")

    # Ensure dictionary exists
    if not ensure_dictionary():
        sys.exit(1)

    safe_print("Smoke test...")
    test_output = run_batch_queries_release(["ngo5"], limit=1)
    results = parse_results(test_output[0] if test_output else "")
    if not results:
        safe_print(f"ERROR: Test query returned no results.")
        sys.exit(1)
    safe_print("Smoke test passed.\n")

    results_log = []

    try:
        for i, penalty in enumerate(penalty_values):
            safe_print(f"\n{'='*60}")
            safe_print(f"[{i+1}/{len(penalty_values)}] UNMATCHED_JYUTPING_PENALTY={penalty}")
            safe_print(f"{'='*60}")

            # Patch
            patched = patch_constant(original_source, penalty)
            write_search_rs(patched)

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

            se = cat_metrics.get("shorter_entry", {})
            ser = cat_metrics.get("shorter_entry_regression", {})
            ms = cat_metrics.get("multi_syllable", {})
            st = cat_metrics.get("single_tone", {})
            pp = cat_metrics.get("partial_prefix", {})

            entry = {
                "penalty": penalty,
                "overall_p1": overall["p@1"],
                "overall_p3": overall["p@3"],
                "overall_mrr": overall["mrr"],
                "overall_not_found": overall["not_found"],
                "se_p1": se.get("p@1", 0),
                "se_p3": se.get("p@3", 0),
                "se_mrr": se.get("mrr", 0),
                "se_not_found": se.get("not_found", 0),
                "se_count": se.get("count", 0),
                "ser_p1": ser.get("p@1", 0),
                "ser_p3": ser.get("p@3", 0),
                "ser_mrr": ser.get("mrr", 0),
                "ms_p1": ms.get("p@1", 0),
                "ms_p3": ms.get("p@3", 0),
                "ms_mrr": ms.get("mrr", 0),
                "ms_not_found": ms.get("not_found", 0),
                "st_p1": st.get("p@1", 0),
                "st_p3": st.get("p@3", 0),
                "st_mrr": st.get("mrr", 0),
                "pp_p1": pp.get("p@1", 0),
                "pp_p3": pp.get("p@3", 0),
                "pp_mrr": pp.get("mrr", 0),
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
            if se:
                safe_print(
                    f"  shorter_entry: p@1={_fmt_pct(se['p@1'])} p@3={_fmt_pct(se['p@3'])} "
                    f"MRR={_fmt_mrr(se['mrr'])} miss={se['not_found']}"
                )
            if ms:
                safe_print(
                    f"  multi_syllable: p@1={_fmt_pct(ms['p@1'])} p@3={_fmt_pct(ms['p@3'])} "
                    f"MRR={_fmt_mrr(ms['mrr'])} miss={ms['not_found']}"
                )
            if st:
                safe_print(
                    f"  single_tone: p@1={_fmt_pct(st['p@1'])} p@3={_fmt_pct(st['p@3'])} "
                    f"MRR={_fmt_mrr(st['mrr'])}"
                )
            if pp:
                safe_print(
                    f"  partial_prefix: p@1={_fmt_pct(pp['p@1'])} p@3={_fmt_pct(pp['p@3'])} "
                    f"MRR={_fmt_mrr(pp['mrr'])}"
                )

    finally:
        # Always restore original source
        safe_print("\nRestoring original search.rs...")
        write_search_rs(original_source)
        safe_print("Restored.")

        # Rebuild with original values (release)
        safe_print("Rebuilding with original values (release)...")
        build_console()
        safe_print("Done.")

    # Save results to experiment folder
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

    # Print summary table
    safe_print(f"\n{'='*100}")
    safe_print("SWEEP SUMMARY")
    safe_print(f"{'='*100}")
    safe_print(
        f"{'Penalty':>8} | {'All p@1':>7} {'All p@3':>7} {'All MRR':>7} {'Miss':>4} | "
        f"{'SE p@1':>7} {'SE p@3':>7} {'SE MRR':>7} | "
        f"{'MS p@1':>7} {'MS MRR':>7} | "
        f"{'ST p@1':>7} {'ST MRR':>7} | "
        f"{'PP p@1':>7} {'PP MRR':>7}"
    )
    safe_print(f"{'-'*8}-+-{'-'*7}-{'-'*7}-{'-'*7}-{'-'*4}-+-{'-'*7}-{'-'*7}-{'-'*7}-+-{'-'*7}-{'-'*7}-+-{'-'*7}-{'-'*7}-+-{'-'*7}-{'-'*7}")

    for r in results_log:
        if "error" in r:
            safe_print(f"{r['penalty']:>8} | {'ERROR':>7}")
            continue
        safe_print(
            f"{r['penalty']:>8} | "
            f"{_fmt_pct(r['overall_p1']):>7} {_fmt_pct(r['overall_p3']):>7} {_fmt_mrr(r['overall_mrr']):>7} {r['overall_not_found']:>4} | "
            f"{_fmt_pct(r['se_p1']):>7} {_fmt_pct(r['se_p3']):>7} {_fmt_mrr(r['se_mrr']):>7} | "
            f"{_fmt_pct(r['ms_p1']):>7} {_fmt_mrr(r['ms_mrr']):>7} | "
            f"{_fmt_pct(r['st_p1']):>7} {_fmt_mrr(r['st_mrr']):>7} | "
            f"{_fmt_pct(r['pp_p1']):>7} {_fmt_mrr(r['pp_mrr']):>7}"
        )

    valid = [r for r in results_log if "error" not in r]
    if valid:
        best_overall = max(valid, key=lambda r: r["overall_mrr"])
        best_se = max(valid, key=lambda r: r["se_mrr"])
        safe_print(f"\nBest overall MRR: penalty={best_overall['penalty']} -> MRR={_fmt_mrr(best_overall['overall_mrr'])}")
        safe_print(f"Best SE MRR:      penalty={best_se['penalty']} -> MRR={_fmt_mrr(best_se['se_mrr'])}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Parameter sweep for CCanto frequency boost constants.

For each (CANTO_HIGH_FREQ_COST, CCANTO_DISCOUNT) pair:
  1. Patch builder.rs with new values
  2. Rebuild console (cargo build --release)
  3. Rebuild dictionary (console.exe build)
  4. Run eval (full suite)
  5. Collect metrics
  6. Restore original values

Usage:
  python eval/sweep_ccanto.py
"""

import json
import re
import subprocess
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
BUILDER_RS = PROJECT_DIR / "dictlib" / "src" / "builder.rs"
CONSOLE_DIR = PROJECT_DIR / "console"
RESULTS_DIR = SCRIPT_DIR / "results"
DICT_PATH = PROJECT_DIR / "full" / "full.jyp_dict"
DOCS_DICT_PATH = PROJECT_DIR / "docs" / "full.jyp_dict"

RELEASE_EXE = CONSOLE_DIR / "target" / "release" / "console.exe"

# Import eval functions
sys.path.insert(0, str(SCRIPT_DIR))
import run_eval
from run_eval import (
    parse_results, evaluate_query,
    compute_metrics, compute_category_metrics, load_query_sets,
    safe_print, _fmt_pct, _fmt_mrr,
)


def read_builder_rs():
    with open(BUILDER_RS, "r", encoding="utf-8") as f:
        return f.read()


def write_builder_rs(content):
    with open(BUILDER_RS, "w", encoding="utf-8") as f:
        f.write(content)


def patch_constants(content, canto_cost, ccanto_discount):
    """Replace the two constants in builder.rs source code."""
    content = re.sub(
        r"pub const CANTO_HIGH_FREQ_COST:\s*u32\s*=\s*[\d_]+;",
        f"pub const CANTO_HIGH_FREQ_COST: u32 = {canto_cost};",
        content,
    )
    content = re.sub(
        r"pub const CCANTO_DISCOUNT:\s*u32\s*=\s*[\d_]+;",
        f"pub const CCANTO_DISCOUNT: u32 = {ccanto_discount};",
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


def build_dictionary():
    """Rebuild the dictionary index. Returns True on success."""
    result = subprocess.run(
        [str(RELEASE_EXE), "build"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=str(CONSOLE_DIR),
        timeout=300,
    )
    if result.returncode != 0:
        safe_print(f"DICT BUILD FAILED:\n{result.stderr[-500:]}")
        return False
    # Print key lines from build output
    for line in result.stdout.splitlines():
        if "Added" in line or "character cost overrides" in line or "Writing done" in line:
            safe_print(f"  {line}")
    return True


def run_batch_queries_release(queries, limit=10):
    """Run batch queries using the release exe."""
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

    blocks = result.stdout.split("===QUERY_END===")
    outputs = []
    for i in range(len(queries)):
        if i < len(blocks):
            outputs.append(blocks[i])
        else:
            outputs.append("")
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
    canto_cost_values = [1_000, 2_000, 3_000, 4_000]
    ccanto_discount_values = [0, 1_000, 2_000, 3_000]

    pairs = []
    for cc in canto_cost_values:
        for cd in ccanto_discount_values:
            pairs.append((cc, cd))

    safe_print(f"CCanto boost sweep: {len(pairs)} combinations")
    safe_print(f"  CANTO_HIGH_FREQ_COST: {canto_cost_values}")
    safe_print(f"  CCANTO_DISCOUNT: {ccanto_discount_values}")

    # Load test cases once
    test_cases = load_query_sets()
    safe_print(f"Loaded {len(test_cases)} test cases")

    # Save original source
    original_source = read_builder_rs()

    results_log = []

    try:
        for i, (cc_val, cd_val) in enumerate(pairs):
            safe_print(f"\n{'='*60}")
            safe_print(f"[{i+1}/{len(pairs)}] CANTO_HIGH_FREQ_COST={cc_val}, CCANTO_DISCOUNT={cd_val}")
            safe_print(f"{'='*60}")

            # Patch
            patched = patch_constants(original_source, cc_val, cd_val)
            write_builder_rs(patched)

            # Build console
            safe_print("Building (release)...")
            t0 = time.time()
            if not build_console():
                safe_print("SKIP (build failed)")
                results_log.append({
                    "canto_cost": cc_val,
                    "ccanto_discount": cd_val,
                    "error": "build_failed",
                })
                continue
            build_time = time.time() - t0
            safe_print(f"Built in {build_time:.1f}s")

            # Rebuild dictionary
            safe_print("Rebuilding dictionary...")
            t0 = time.time()
            if not build_dictionary():
                safe_print("SKIP (dict build failed)")
                results_log.append({
                    "canto_cost": cc_val,
                    "ccanto_discount": cd_val,
                    "error": "dict_build_failed",
                })
                continue
            dict_time = time.time() - t0
            safe_print(f"Dictionary built in {dict_time:.1f}s")

            # Run eval
            safe_print("Evaluating...")
            t0 = time.time()
            eval_results, overall, cat_metrics = do_eval(test_cases)
            eval_time = time.time() - t0
            safe_print(f"Evaluated in {eval_time:.1f}s")

            # Extract ccanto_boost category
            ccb = cat_metrics.get("ccanto_boost", {})
            # Also get cantonese_vocab for comparison
            cv = cat_metrics.get("cantonese_vocab", {})

            entry = {
                "canto_cost": cc_val,
                "ccanto_discount": cd_val,
                "overall_p1": overall["p@1"],
                "overall_p3": overall["p@3"],
                "overall_mrr": overall["mrr"],
                "overall_not_found": overall["not_found"],
                "ccb_p1": ccb.get("p@1", 0),
                "ccb_p3": ccb.get("p@3", 0),
                "ccb_mrr": ccb.get("mrr", 0),
                "ccb_not_found": ccb.get("not_found", 0),
                "ccb_count": ccb.get("count", 0),
                "cv_p1": cv.get("p@1", 0),
                "cv_p3": cv.get("p@3", 0),
                "cv_mrr": cv.get("mrr", 0),
                "build_time": build_time,
                "dict_time": dict_time,
                "eval_time": eval_time,
            }

            # Per-category summary
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
            if ccb:
                safe_print(
                    f"  ccanto_boost: p@1={_fmt_pct(ccb['p@1'])} p@3={_fmt_pct(ccb['p@3'])} "
                    f"MRR={_fmt_mrr(ccb['mrr'])} miss={ccb['not_found']}"
                )

    finally:
        # Always restore original source
        safe_print("\nRestoring original builder.rs...")
        write_builder_rs(original_source)
        safe_print("Restored.")

        # Rebuild with original values
        safe_print("Rebuilding with original values (release)...")
        build_console()
        safe_print("Rebuilding dictionary with original values...")
        build_dictionary()
        # Copy rebuilt dictionary to docs
        if DICT_PATH.exists():
            shutil.copy2(DICT_PATH, DOCS_DICT_PATH)
            safe_print("Dictionary copied to docs/.")
        safe_print("Done.")

    # Save results
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    sweep_path = RESULTS_DIR / "sweep_ccanto_results.json"
    with open(sweep_path, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "parameters": {
                "canto_cost_values": canto_cost_values,
                "ccanto_discount_values": ccanto_discount_values,
            },
            "results": results_log,
        }, f, indent=2)
    safe_print(f"\nSweep results saved to: {sweep_path}")

    # Print summary table
    safe_print(f"\n{'='*90}")
    safe_print("SWEEP SUMMARY")
    safe_print(f"{'='*90}")
    safe_print(
        f"{'CC':>6} {'CD':>6} | {'All p@1':>7} {'All p@3':>7} {'All MRR':>7} {'Miss':>4} | "
        f"{'CCB p@1':>7} {'CCB p@3':>7} {'CCB MRR':>7} {'Miss':>4}"
    )
    safe_print(f"{'-'*6} {'-'*6}-+-{'-'*7}-{'-'*7}-{'-'*7}-{'-'*4}-+-{'-'*7}-{'-'*7}-{'-'*7}-{'-'*4}")

    for r in results_log:
        if "error" in r:
            safe_print(f"{r['canto_cost']:>6} {r['ccanto_discount']:>6} | {'ERROR':>7}")
            continue
        safe_print(
            f"{r['canto_cost']:>6} {r['ccanto_discount']:>6} | "
            f"{_fmt_pct(r['overall_p1']):>7} {_fmt_pct(r['overall_p3']):>7} {_fmt_mrr(r['overall_mrr']):>7} {r['overall_not_found']:>4} | "
            f"{_fmt_pct(r['ccb_p1']):>7} {_fmt_pct(r['ccb_p3']):>7} {_fmt_mrr(r['ccb_mrr']):>7} {r['ccb_not_found']:>4}"
        )

    # Find best
    valid = [r for r in results_log if "error" not in r]
    if valid:
        best_overall = max(valid, key=lambda r: r["overall_mrr"])
        best_ccb = max(valid, key=lambda r: r["ccb_mrr"])
        safe_print(f"\nBest overall MRR: CC={best_overall['canto_cost']} CD={best_overall['ccanto_discount']} "
                    f"-> MRR={_fmt_mrr(best_overall['overall_mrr'])}")
        safe_print(f"Best CCB MRR:     CC={best_ccb['canto_cost']} CD={best_ccb['ccanto_discount']} "
                    f"-> MRR={_fmt_mrr(best_ccb['ccb_mrr'])}")


if __name__ == "__main__":
    main()

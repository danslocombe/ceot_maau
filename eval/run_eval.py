#!/usr/bin/env python3
"""
Jyutping Dictionary Ranking Evaluation Script

Runs queries against the console app and evaluates results against expected values.
Generates a markdown report with pass/fail per query, category-level pass rates,
cost breakdowns for failures, and pattern analysis.
"""

import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
QUERY_SET_PATH = SCRIPT_DIR / "query_set.json"
RESULTS_DIR = SCRIPT_DIR / "results"
REPORT_PATH = RESULTS_DIR / "report.md"
CONSOLE_EXE = SCRIPT_DIR.parent / "console" / "target" / "debug" / "console.exe"
CONSOLE_DIR = SCRIPT_DIR.parent / "console"


def run_query(query: str, limit: int = 10) -> str:
    """Run a single query against the console app and return raw output."""
    cmd = [str(CONSOLE_EXE), "--query", query, "--limit", str(limit)]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
            cwd=str(CONSOLE_DIR),
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        return f"TIMEOUT for query: {query}"
    except Exception as e:
        return f"ERROR: {e}"


def parse_results(output: str) -> list[dict]:
    """Parse the Rust Debug output format into structured results.

    The output format looks like:
    (Match MatchWithHitInfo { match_obj: Match { cost_info: MatchCostInfo { term_match_cost: N, ... }, ... }, ... })
    DisplayDictionaryEntry {
        characters: "...",
        jyutping: "...",
        english_definitions: [...],
        cost: N,
        entry_source: CEDict|CCanto,
    }
    """
    results = []

    # Split into match blocks - each starts with "(Match MatchWithHitInfo"
    match_blocks = re.split(r"\(Match MatchWithHitInfo", output)

    for block in match_blocks[1:]:  # Skip the header before first match
        entry = {}

        # Extract cost info
        term_match = re.search(r"term_match_cost:\s*(\d+)", block)
        unmatched_match = re.search(r"unmatched_position_cost:\s*(\d+)", block)
        inversion_match = re.search(r"inversion_cost:\s*(\d+)", block)
        static_match = re.search(r"static_cost:\s*(\d+)", block)

        if term_match:
            entry["term_match_cost"] = int(term_match.group(1))
        if unmatched_match:
            entry["unmatched_position_cost"] = int(unmatched_match.group(1))
        if inversion_match:
            entry["inversion_cost"] = int(inversion_match.group(1))
        if static_match:
            entry["static_cost"] = int(static_match.group(1))

        entry["total_cost"] = (
            entry.get("term_match_cost", 0)
            + entry.get("unmatched_position_cost", 0)
            + entry.get("inversion_cost", 0)
            + entry.get("static_cost", 0)
        )

        # Extract match type
        match_type_m = re.search(r"match_type:\s*(Jyutping|Traditional|English)", block)
        if match_type_m:
            entry["match_type"] = match_type_m.group(1)

        # Extract entry_id
        entry_id_m = re.search(r"entry_id:\s*(\d+)", block)
        if entry_id_m:
            entry["entry_id"] = int(entry_id_m.group(1))

        # Extract DisplayDictionaryEntry fields
        chars_m = re.search(r'characters:\s*"([^"]*)"', block)
        if chars_m:
            entry["characters"] = chars_m.group(1)

        jyutping_m = re.search(r'jyutping:\s*"([^"]*)"', block)
        if jyutping_m:
            entry["jyutping"] = jyutping_m.group(1)

        # Extract english_definitions as a list
        defs_block_m = re.search(
            r"english_definitions:\s*\[(.*?)\]", block, re.DOTALL
        )
        if defs_block_m:
            defs_raw = defs_block_m.group(1)
            defs = re.findall(r'"((?:[^"\\]|\\.)*)"', defs_raw)
            entry["english_definitions"] = defs
        else:
            entry["english_definitions"] = []

        # Extract cost (from DisplayDictionaryEntry)
        display_cost_m = re.search(r"cost:\s*(\d+),\s*\n\s*entry_source", block)
        if display_cost_m:
            entry["display_cost"] = int(display_cost_m.group(1))

        # Extract entry_source
        source_m = re.search(r"entry_source:\s*(CEDict|CCanto)", block)
        if source_m:
            entry["entry_source"] = source_m.group(1)

        if entry.get("characters"):
            results.append(entry)

    return results


def strip_html(text: str) -> str:
    """Remove HTML markup from a string."""
    return re.sub(r"<[^>]+>", "", text)


def evaluate_query(test_case: dict, results: list[dict]) -> dict:
    """Evaluate a single query's results against expectations."""
    eval_result = {
        "id": test_case["id"],
        "query": test_case["query"],
        "category": test_case["category"],
        "description": test_case["description"],
        "passed": False,
        "reason": "",
        "top_results": [],
        "match_details": None,
    }

    if not results:
        eval_result["reason"] = "No results returned"
        return eval_result

    accept_top_n = test_case.get("accept_top_n", 3)
    top_results = results[:accept_top_n]

    # Store top results for reporting
    for r in results[:5]:
        eval_result["top_results"].append({
            "characters": strip_html(r.get("characters", "")),
            "jyutping": strip_html(r.get("jyutping", "")),
            "total_cost": r.get("total_cost", 0),
            "static_cost": r.get("static_cost", 0),
            "term_match_cost": r.get("term_match_cost", 0),
            "unmatched_position_cost": r.get("unmatched_position_cost", 0),
            "match_type": r.get("match_type", ""),
            "entry_source": r.get("entry_source", ""),
        })

    # Check if any expected character is in the top N results
    expected_chars = test_case.get("expected_characters", [])
    expected_jyutping = test_case.get("expected_jyutping", [])
    definition_contains = test_case.get("definition_contains", [])

    found = False
    for r in top_results:
        r_chars = strip_html(r.get("characters", ""))
        r_jyutping = strip_html(r.get("jyutping", ""))

        # Check character match
        if expected_chars:
            for exp_char in expected_chars:
                if r_chars == exp_char:
                    found = True
                    eval_result["match_details"] = {
                        "matched_on": "character",
                        "matched_value": exp_char,
                        "position": top_results.index(r) + 1,
                    }
                    break

        # Check jyutping match (if no character match yet)
        if not found and expected_jyutping:
            for exp_jp in expected_jyutping:
                if r_jyutping == exp_jp:
                    found = True
                    eval_result["match_details"] = {
                        "matched_on": "jyutping",
                        "matched_value": exp_jp,
                        "position": top_results.index(r) + 1,
                    }
                    break

        # Check definition contains
        if not found and definition_contains:
            defs = " ".join(r.get("english_definitions", []))
            for kw in definition_contains:
                if kw.lower() in defs.lower():
                    found = True
                    eval_result["match_details"] = {
                        "matched_on": "definition",
                        "matched_value": kw,
                        "position": top_results.index(r) + 1,
                    }
                    break

        if found:
            break

    eval_result["passed"] = found
    if not found:
        actual_chars = [strip_html(r.get("characters", "")) for r in top_results]
        actual_jp = [strip_html(r.get("jyutping", "")) for r in top_results]
        eval_result["reason"] = (
            f"Expected one of {expected_chars} but got {actual_chars} "
            f"(jyutping: {actual_jp})"
        )

    return eval_result


def generate_report(eval_results: list[dict], test_cases: list[dict]) -> str:
    """Generate a markdown report from evaluation results."""
    lines = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    total = len(eval_results)
    passed = sum(1 for r in eval_results if r["passed"])
    failed = total - passed

    lines.append(f"# Dictionary Ranking Evaluation Report")
    lines.append(f"")
    lines.append(f"Generated: {now}")
    lines.append(f"")
    lines.append(f"## Summary")
    lines.append(f"")
    lines.append(f"- **Total queries**: {total}")
    lines.append(f"- **Passed**: {passed} ({100*passed/total:.1f}%)")
    lines.append(f"- **Failed**: {failed} ({100*failed/total:.1f}%)")
    lines.append(f"")

    # Category breakdown
    lines.append(f"## Category Results")
    lines.append(f"")
    lines.append(f"| Category | Total | Passed | Failed | Pass Rate |")
    lines.append(f"|----------|-------|--------|--------|-----------|")

    categories = defaultdict(lambda: {"total": 0, "passed": 0})
    for r in eval_results:
        cat = r["category"]
        categories[cat]["total"] += 1
        if r["passed"]:
            categories[cat]["passed"] += 1

    cat_order = [
        "single_tone", "single_no_tone", "multi_syllable",
        "cantonese_vocab", "partial_prefix", "english",
        "character", "edge_case",
    ]
    for cat in cat_order:
        if cat in categories:
            d = categories[cat]
            rate = 100 * d["passed"] / d["total"] if d["total"] > 0 else 0
            failed_cat = d["total"] - d["passed"]
            lines.append(
                f"| {cat} | {d['total']} | {d['passed']} | {failed_cat} | {rate:.0f}% |"
            )

    lines.append(f"")

    # Detailed failures
    failures = [r for r in eval_results if not r["passed"]]
    if failures:
        lines.append(f"## Failed Queries ({len(failures)})")
        lines.append(f"")

        for r in failures:
            lines.append(f"### #{r['id']}: `{r['query']}` ({r['category']})")
            lines.append(f"")
            lines.append(f"**Description**: {r['description']}")
            lines.append(f"")
            lines.append(f"**Reason**: {r['reason']}")
            lines.append(f"")

            if r["top_results"]:
                lines.append(f"**Top results:**")
                lines.append(f"")
                lines.append(
                    f"| # | Characters | Jyutping | Total Cost | Static | Term Match | Unmatched | Type | Source |"
                )
                lines.append(
                    f"|---|-----------|----------|------------|--------|------------|-----------|------|--------|"
                )
                for i, tr in enumerate(r["top_results"], 1):
                    lines.append(
                        f"| {i} | {tr['characters']} | {tr['jyutping']} | "
                        f"{tr['total_cost']} | {tr['static_cost']} | "
                        f"{tr['term_match_cost']} | {tr['unmatched_position_cost']} | "
                        f"{tr['match_type']} | {tr['entry_source']} |"
                    )
                lines.append(f"")

    # Pattern analysis
    lines.append(f"## Pattern Analysis")
    lines.append(f"")

    # CCanto vs CEDict issue analysis
    ccanto_wins = 0
    cedict_wins = 0
    ccanto_loses_to_partial = 0

    for r in eval_results:
        if not r["top_results"]:
            continue
        top = r["top_results"][0]
        if top["entry_source"] == "CCanto":
            ccanto_wins += 1
        elif top["entry_source"] == "CEDict":
            cedict_wins += 1

    for r in failures:
        if not r["top_results"]:
            continue
        top = r["top_results"][0]
        if top["term_match_cost"] > 0 and top["entry_source"] == "CEDict":
            ccanto_loses_to_partial += 1

    lines.append(f"### Source Distribution in Top Results")
    lines.append(f"")
    lines.append(f"- CCanto as top result: {ccanto_wins}")
    lines.append(f"- CEDict as top result: {cedict_wins}")
    lines.append(f"")

    lines.append(f"### Failure Patterns")
    lines.append(f"")

    # Exact match losing to partial match
    exact_loses = 0
    high_static_cost = 0
    for r in failures:
        if not r["top_results"]:
            continue
        top = r["top_results"][0]
        if top["term_match_cost"] > 0:
            exact_loses += 1
        if top["static_cost"] > 15000:
            high_static_cost += 1

    lines.append(f"- Failures where top result has term_match_cost > 0 (partial/fuzzy match winning): {exact_loses}")
    lines.append(f"- Failures where top result has static_cost > 15000 (high base cost): {high_static_cost}")
    lines.append(f"- Failures where CEDict partial match beats CCanto exact match: {ccanto_loses_to_partial}")
    lines.append(f"")

    # Static cost distribution in failures
    if failures:
        lines.append(f"### Cost Distribution in Failures")
        lines.append(f"")
        lines.append(f"| Query | Expected | Got | Got Total Cost | Got Static | Got Source |")
        lines.append(f"|-------|----------|-----|----------------|------------|-----------|")
        for r in failures[:30]:  # Limit to first 30
            tc = next((t for t in test_cases if t["id"] == r["id"]), None)
            if tc and r["top_results"]:
                top = r["top_results"][0]
                expected = ", ".join(tc.get("expected_characters", []))
                lines.append(
                    f"| `{r['query']}` | {expected} | {top['characters']} | "
                    f"{top['total_cost']} | {top['static_cost']} | {top['entry_source']} |"
                )
        lines.append(f"")

    # All results detail
    lines.append(f"## All Results")
    lines.append(f"")
    lines.append(f"| # | Query | Status | Top Char | Top JP | Total Cost | Source |")
    lines.append(f"|---|-------|--------|----------|--------|------------|--------|")

    for r in eval_results:
        status = "PASS" if r["passed"] else "FAIL"
        if r["top_results"]:
            top = r["top_results"][0]
            lines.append(
                f"| {r['id']} | `{r['query']}` | {status} | "
                f"{top['characters']} | {top['jyutping']} | "
                f"{top['total_cost']} | {top['entry_source']} |"
            )
        else:
            lines.append(
                f"| {r['id']} | `{r['query']}` | {status} | - | - | - | - |"
            )

    lines.append(f"")
    return "\n".join(lines)


def safe_print(*args, **kwargs):
    """Print with UTF-8 encoding fallback."""
    try:
        print(*args, **kwargs)
    except UnicodeEncodeError:
        text = " ".join(str(a) for a in args)
        sys.stdout.buffer.write(text.encode("utf-8", errors="replace"))
        if kwargs.get("end", "\n") == "\n":
            sys.stdout.buffer.write(b"\n")
        sys.stdout.buffer.flush()


def main():
    # Load test cases
    with open(QUERY_SET_PATH, "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    print(f"Loaded {len(test_cases)} test cases")

    # Check console exe exists
    if not CONSOLE_EXE.exists():
        print(f"ERROR: Console exe not found at {CONSOLE_EXE}")
        print("Run: cd console && cargo build")
        sys.exit(1)

    # Run all queries
    eval_results = []
    for i, tc in enumerate(test_cases):
        query = tc["query"]
        safe_print(f"  [{i+1}/{len(test_cases)}] Testing: {query}", end="")

        raw_output = run_query(query, limit=10)
        results = parse_results(raw_output)
        eval_result = evaluate_query(tc, results)
        eval_results.append(eval_result)

        status = "PASS" if eval_result["passed"] else "FAIL"
        safe_print(f" -> {status}")

    # Generate report
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    report = generate_report(eval_results, test_cases)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report)

    # Print summary
    passed = sum(1 for r in eval_results if r["passed"])
    total = len(eval_results)
    print(f"\n{'='*50}")
    print(f"Results: {passed}/{total} passed ({100*passed/total:.1f}%)")
    print(f"Report written to: {REPORT_PATH}")

    # Also save raw results as JSON for later comparison
    raw_results_path = RESULTS_DIR / "raw_results.json"
    with open(raw_results_path, "w", encoding="utf-8") as f:
        json.dump(eval_results, f, indent=2, ensure_ascii=False)
    print(f"Raw results written to: {raw_results_path}")


if __name__ == "__main__":
    main()

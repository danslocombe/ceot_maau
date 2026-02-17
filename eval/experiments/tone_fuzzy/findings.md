# Tone-Fuzzy Matching Experiment: Findings

## Summary

**Recommendation: Keep JYUTPING_TONE_MISMATCH_PENALTY = 16,000.**

This adds tone-fuzzy matching — queries with incorrect tones now find results instead
of returning nothing. 7 of 8 tone-mismatch test cases appear at position 1, and all 8
appear in top 3. No significant regressions in existing categories.

## What Changed

### Core change: tone mismatch as penalty, not rejection

Previously, if a query specified a tone (e.g., `man2`), only entries with that exact
tone matched. If the dictionary has `man4`, the entry was completely invisible.

Now, tone-mismatched entries are accepted but penalized:
- Exact tone match: +0 cost (unchanged)
- Tone mismatch: +16,000 cost per syllable

This means tone-mismatched entries rank below exact-tone matches but above "not found."

### Files modified

| File | Change |
|------|--------|
| `dictlib/src/search.rs` | Added `JYUTPING_TONE_MISMATCH_PENALTY` constant (16,000). Modified `matches_jyutping_term()` to accept tone mismatches with penalty. Fixed position double-match bug (see below). |
| `dictlib/src/reconstruct_match.rs` | Updated `get_jyutping_best_match()` to accept tone mismatches. Updated span highlighting to show base match without tone digit for mismatched entries. |

## Sweep Results

Swept `JYUTPING_TONE_MISMATCH_PENALTY` over [5,000, 8,000, 12,000, 16,000, 24,000].
All release build, 758 test cases (745 existing + 13 new tone_fuzzy).

| Penalty | Overall p@1 | Overall MRR | Miss | TF p@1 | TF p@3 | TFN p@1 | ST p@1 | MS p@1 | EVP p@1 |
|---------|-------------|-------------|------|--------|--------|---------|--------|--------|---------|
| 5,000   | 88.4%       | 0.927       | 11   | 100%   | 100%   | 50%     | 87%    | 96%    | 77%     |
| 8,000   | 94.1%       | 0.961       | 10   | 100%   | 100%   | 50%     | 99%    | 96%    | 93%     |
| **12,000** | 94.1%    | 0.961       | 10   | 88%    | 100%   | 100%    | 99%    | 96%    | 93%     |
| **16,000** | **94.3%** | **0.962**  | **10** | **88%** | **100%** | **100%** | **99%** | **97%** | **93%** |
| 24,000  | 94.3%       | 0.963       | 9    | 88%    | 100%   | 100%    | 99%    | 97%    | 93%     |

### Key observations

1. **5,000 is catastrophic**: Tone-mismatched entries flood results, single_tone drops
   from 99% to 87%, exact_vs_prefix drops from 93% to 77%.

2. **8,000 breaks negative cases**: `gam1` (今) is beaten by `gam2` (錦) because the
   8,000 penalty isn't enough to overcome static_cost differences. All tone-fuzzy cases
   pass at p@1, but at the cost of wrong results for exact-tone queries.

3. **12,000 is the threshold**: Negative cases pass (exact-tone always wins), tone-fuzzy
   drops to 88% p@1 (1 case at position 2, all 8 in top 3). But multi_syllable stays
   at 96% (slightly below baseline's 97-98%).

4. **16,000 is the sweet spot**: Same tone-fuzzy performance as 12,000, but multi_syllable
   recovers to 97%. All other categories match or exceed baseline levels.

5. **24,000 is marginally better overall** (1 fewer not-found) but tone-fuzzy MRR drops
   (the non-p@1 case moves from position 2 to position 3).

### Why 16,000?

The penalty of 16,000 ensures:
- A tone mismatch costs more than `JYUTPING_NON_PERFECT_MATCH` (6,000) + typical
  `COMPLETION_PENALTY` (4,000-8,000), so exact-tone prefix matches beat tone-mismatched
  exact matches
- A tone mismatch costs more than `UNMATCHED_JYUTPING_PENALTY` for 1 extra syllable
  (10,000), so a 2-char exact-tone entry beats a 1-char tone-mismatched entry
- Two tone mismatches (32,000) effectively push multi-syllable entries far down,
  preventing nonsensical results where both syllables have wrong tones

## Tone-Fuzzy Test Cases

| ID  | Query | Expected | Penalty=16K |
|-----|-------|----------|-------------|
| 800 | `jing1 man2` | 英文 (man4) | p@1 |
| 801 | `zung1 man2` | 中文 (man4) | p@1 |
| 802 | `soeng5 min6` | 上面 (soeng6) | p@1 |
| 803 | `haa5 min6` | 下面 (haa6) | p@1 |
| 804 | `haa5 ci3` | 下次 (haa6) | p@1 |
| 805 | `gam1 nin2` | 今年 (nin4) | p@1 |
| 806 | `ji1 ging1` | 已經 (ji5) | p@2 |
| 807 | `jau4 guk2` | 郵局 (guk6) | p@1 |

Case 806 (`ji1 ging1` → 已經) drops to position 2 because `ji1` matches entries like
紀 (gei2→ji→similar) that have lower static cost, pushing 已經 down by one.

## Bug fix: position double-matching

During testing, the debug build panicked (`debug_assert!(false)` in reconstruct_match.rs)
while the release build worked fine. Investigation revealed the root cause:

**Problem:** `matches_jyutping_term()` allows two query terms to greedily match the same
entry jyutping position. `get_jyutping_best_match()` (used for span highlighting) correctly
prevents reuse via BFS — when the greedy matcher finds a match but the BFS can't
reconstruct it, the `debug_assert!(false)` fires.

**Example:** Query `jat1 jat6` on entry `一係` (jat1 hai6):
- Term 1 (`jat1`): matches position 0 (exact tone)
- Term 2 (`jat6`): matches position 0 (tone mismatch on jat1) — only option since `hai` ≠ `jat`
- Both claim position 0 → greedy says "match" but BFS says "impossible"

**Pre-existing but hidden:** This bug existed before tone-fuzzy matching, but was extremely
unlikely because two query terms rarely shared the same exact base+tone. With tone-fuzzy
matching, any two query terms with the same base can now both match the same position
(one exact, one with tone mismatch), making the bug much more common.

**Fix:** Added a check in `matches_jyutping_term()` to skip positions already claimed by
a previous query term (using the existing `entry_jyutping_matches` BitSet).

**Impact:** Debug build not-found dropped from 17 → 9. Debug and release builds now produce
consistent results. Several multi-syllable queries that were crashing in debug mode
(e.g., `jat1 jat6`, `baai1 baai3`, `daa2 din6 waa2`) now work correctly.

## Cumulative Progress

| Metric | Start of experiments | After tone_fuzzy |
|--------|---------------------|-----------------|
| Overall p@1 | 88% | 94% |
| Overall MRR | ~0.91 | 0.96 |
| Not found | ~22 | 9 |
| Test cases | 650 | 758 |

Tone-fuzzy matching adds 8 previously-impossible queries to the success pool while
maintaining or improving all other category metrics. The position double-match bugfix
additionally recovered 8 entries that were lost to debug panics.

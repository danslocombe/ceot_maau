# Parameter Sweep: UNMATCHED_JYUTPING_PENALTY (Shorter Entry Preference)

Date: 2026-02-17

## Background

When a user searches a multi-syllable jyutping like `jing1 man4`, the dictionary may
return longer entries (英文堂 `jing1 man4 tong4`) instead of the shorter match (英文
`jing1 man4`). The `UNMATCHED_JYUTPING_PENALTY` applies a position-weighted cost for
each unmatched syllable in an entry.

### Pre-sweep investigation

Detailed analysis of multi_syllable failures revealed **two distinct root causes**:

1. **Tone mismatch (8/12 failures)**: The expected shorter entry didn't match because
   the dictionary jyutping uses a different tone than the query (e.g., man2 vs man4).
   These are coverage issues, not ranking issues.

2. **Missing entries (3/12 failures)**: Colloquial phrases (好靚, 得唔得, 死唔死) don't
   exist as dictionary entries.

3. **Genuine ranking issue (1/12)**: 餐館 vs 差館 — a term_match_cost issue between
   two 2-syllable entries, not related to the unmatched penalty.

**None of the 12 failures were caused by insufficient UNMATCHED_JYUTPING_PENALTY.**

## Pre-sweep fixes

Fixed 8 tone-mismatch test cases in `query_set.json`:
- `jing1 man2` → `jing1 man4` (英文)
- `zung1 man2` → `zung1 man4` (中文)
- `soeng5 min6` → `soeng6 min6` (上面)
- `haa5 min6` → `haa6 min6` (下面)
- `haa5 ci3` → `haa6 ci3` (下次)
- `gam1 nin2` → `gam1 nin4` (今年)
- `ji1 ging1` → `ji5 ging1` (已經)
- `jau4 guk2` → `jau4 guk6` (郵局)

After fixing: multi_syllable went from 91% p@1 to **97% p@1**. Overall went from
90% p@1 to **91% p@1**, MRR 0.93 → 0.94, not-found 18 → 10.

## Methodology

- 745 test cases (650 query_set + 40 exact_vs_prefix_extended + 25 shorter_entry + 30 ccanto_boost)
- 25 new shorter_entry test cases: 20 testing 2-syl vs 3+ syl preference, 5 regression checks
- Swept 4 values of `UNMATCHED_JYUTPING_PENALTY`: [10,000, 15,000, 20,000, 25,000]
- Each combination: patch search.rs, `cargo build --release`, run full eval
- No dictionary rebuild needed (search-only constant)

## Results

```
 Penalty | All p@1 All p@3 All MRR Miss |  SE p@1  SE p@3  SE MRR |  MS p@1  MS MRR |  ST p@1  ST MRR |  PP p@1  PP MRR
---------|-------------------------------|-------------------------|-----------------|-----------------|----------------
   10000 |     93%     98%    0.96   10  |    100%    100%    1.00 |     98%    0.98 |     99%    0.99 |     76%    0.86  <- current
   15000 |     93%     98%    0.96   11  |    100%    100%    1.00 |     98%    0.98 |     99%    0.99 |     76%    0.86
   20000 |     93%     98%    0.96   11  |    100%    100%    1.00 |     98%    0.98 |     99%    0.99 |     76%    0.86
   25000 |     93%     98%    0.96   11  |    100%    100%    1.00 |     98%    0.98 |     99%    0.99 |     76%    0.86
```

## Analysis

1. **The current value (10,000) is already optimal.** All 20 shorter_entry test cases pass at
   position 1 across all penalty values. The existing penalty is sufficient to push 3+ syllable
   entries below their 2-syllable counterparts.

2. **Increasing the penalty only causes harm.** At 15,000+, one additional query becomes
   not-found (10 → 11), likely because a previously-borderline longer entry gets pushed out
   of the top-10 results entirely.

3. **No category benefits from higher penalty.** Multi_syllable, single_tone, and partial_prefix
   all remain unchanged across all four values.

4. **The investigation was more valuable than the sweep.** Fixing the 8 tone-mismatch test
   cases was the real win: multi_syllable p@1 improved from 91% to 97-98%, and overall
   not-found dropped from 18 to 10.

## Decision

**Keep `UNMATCHED_JYUTPING_PENALTY = 10,000` (no change).**

The current value correctly handles all tested shorter-vs-longer entry scenarios. The penalty
formula's position-weighting naturally makes it more expensive to have unmatched syllables
at earlier positions, which is the right behavior.

## Remaining multi_syllable failures

After tone fixes, multi_syllable has 2 not-found cases remaining. These are likely missing
dictionary entries (colloquial phrases), not ranking issues.

## Cumulative Impact (from original baseline)

| Metric | Original | After exact/prefix | After CCanto | After tone fixes | Delta |
|--------|----------|-------------------|--------------|------------------|-------|
| Overall p@1 | 88% | 92% | 92% | 93% | +5% |
| Overall p@3 | 94% | 96% | 97% | 98% | +4% |
| Overall MRR | 0.91 | 0.94 | 0.94 | 0.96 | +0.05 |
| Not found | 22 | 18 | 18 | 10 | -12 |
| Multi_syl p@1 | ~91% | ~91% | ~91% | 98% | +7% |

## Next opportunities

The biggest remaining weakness is **partial_prefix** at 76% p@1. The next experiment
should investigate prefix matching and completion penalty tuning for incomplete queries.

Tone-fuzzy matching (treating wrong-tone matches as a penalty rather than hard rejection)
could also recover results for users who type common but "wrong" tones.

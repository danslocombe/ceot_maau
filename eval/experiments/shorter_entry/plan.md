# Experiment Plan: Shorter Entry Preference for Multi-Syllable Queries

## Problem

When a user searches a multi-syllable jyutping like `jing1 man2`, the dictionary returns
longer entries (英文堂 `jing1 man2 tong4`) instead of the expected shorter match (英文
`jing1 man2`). The longer entry matches all query syllables perfectly but has unmatched
extra syllables that receive an insufficient penalty.

### Root Cause Investigation

The `multi_syllable` category has 140 test cases with **91% p@1, 11 not-found**. Detailed
analysis of the 12 failures reveals **two distinct root causes**:

#### Root Cause 1: Tone mismatch (8/12 failures)

Most failures are NOT caused by the unmatched penalty — the expected shorter entry simply
doesn't match because it has a different tone in its jyutping annotation:

| Query | Expected | Dict jyutping | Tone issue |
|-------|----------|--------------|------------|
| jing1 man2 | 英文 | jing1 man**4** | man2 vs man4 |
| zung1 man2 | 中文 | zung1 man**4** | man2 vs man4 |
| soeng5 min6 | 上面 | soeng**6** min6 | soeng5 vs soeng6 |
| haa5 min6 | 下面 | haa**6** min6 | haa5 vs haa6 |
| haa5 ci3 | 下次 | haa**6** ci3 | haa5 vs haa6 |
| gam1 nin2 | 今年 | gam1 nin**4** | nin2 vs nin4 |
| ji1 ging1 | 已經 | ji**5** ging1 | ji1 vs ji5 |
| jau4 guk2 | 郵局 | jau4 guk**6** | guk2 vs guk6 |

The expected entries exist in CEDict with correct characters, but the jyutping annotation
(from `cccedict-canto-readings-150923.txt`) uses a different tone than what users commonly
type. The longer CCanto entries happen to use the "user-typed" tone variant.

This is a **jyutping coverage issue**, not a ranking issue. Increasing UNMATCHED_JYUTPING_PENALTY
won't fix these cases because the shorter entry never matches the query at all.

#### Root Cause 2: Missing entries (3/12 failures)

| Query | Expected | Status |
|-------|----------|--------|
| hou2 leng3 | 好靚 | No standalone entry in either dictionary |
| dak1 m4 dak1 | 得唔得 | No entry in either dictionary |
| sei2 m4 sei2 | 死唔死 | No entry in either dictionary |

These colloquial Cantonese phrases simply don't exist as dictionary entries.

#### Root Cause 3: Genuine unmatched penalty issue (1/12)

| Query | Expected | Winner | Why winner wins |
|-------|----------|--------|-----------------|
| caai1 gwun2 | 餐館 (caan1 gun2) | 差館 (caai1 gun2) | 差館 has better term_match_cost |

This is actually a term_match_cost issue (partial match penalty), not an unmatched penalty
issue. Both are 2-syllable entries.

### The unmatched penalty formula

In `search.rs` lines 369-374:
```rust
for i in 0..entry.jyutping.len() {
    if (!entry_jyutping_matches.contains(i)) {
        unmatched_position_cost += ((entry.jyutping.len() + 1) - i) as u32 * UNMATCHED_JYUTPING_PENALTY;
    }
}
```

The penalty is **position-weighted**: earlier unmatched positions are penalized more heavily.
For an entry with N syllables, unmatched position i costs `(N + 1 - i) × PENALTY`.

**Examples with current PENALTY = 10,000:**

| Entry length | Unmatched positions | Total unmatched cost |
|--------------|--------------------|--------------------|
| 3 syllables, query matches [0,1] | [2] | (3+1-2)×10K = **20,000** |
| 4 syllables, query matches [0,1] | [2,3] | (4+1-2)×10K + (4+1-3)×10K = **30K+20K = 50,000** |
| 4 syllables, query matches [2,3] | [0,1] | (4+1-0)×10K + (4+1-1)×10K = **50K+40K = 90,000** |

The formula naturally penalizes prefix matches less than suffix matches (finding query
syllables at positions [2,3] is worse than [0,1]), which is generally correct behavior.

### When the penalty IS effective

For `nei5 hou2` → 你好 (p@1 = position 1):
- 你好: total = 0 + 0 + 18,766 = **18,766**
- 你好嘢: total = 0 + 20,000 + 20,766 = **40,766** (correctly ranked below)
- 你好嗎: total = 0 + 20,000 + 25,766 = **45,766** (correctly ranked below)

The penalty works well here because both short and long entries have similar static_cost,
and the 20,000 unmatched penalty is enough to differentiate.

### When the penalty might be insufficient

The penalty could fail when:
1. The shorter entry has significantly higher static_cost (rare characters)
2. The shorter entry has heavy cost_heuristic penalties (no M:/CL:, no Cantonese)
3. Multiple extra syllables get small individual penalties (last-position weighting)

A 3-syllable entry with 1 unmatched syllable at the end only gets 20,000 penalty.
If the shorter 2-syllable entry has 20,000+ more static_cost, the longer entry wins.

## Proposed Approaches

### Approach A: Increase UNMATCHED_JYUTPING_PENALTY

Increase the per-position penalty so longer entries are more heavily penalized.

**Sweep values:** [10,000 (current), 15,000, 20,000, 25,000]

**Impact at 20,000:**
- 3 syllables, 1 unmatched at end: 20K → **40,000** (+20K)
- 4 syllables, 2 unmatched at end: 50K → **100,000** (+50K)
- 4 syllables, 2 unmatched at start: 90K → **180,000** (+90K)

**Risk:** Higher penalty could over-penalize legitimate longer entries that should
appear for partial queries. For example, searching `nei5` should still show 你好
(nei5 hou2) as a reasonable result.

### Approach B: Add a flat per-extra-syllable penalty

Instead of only the position-weighted penalty, add a flat bonus penalty for each
unmatched syllable, independent of position:

```
total_unmatched = sum_of_position_weighted_costs + NUM_UNMATCHED * FLAT_PENALTY
```

This would make the penalty less sensitive to position and more about the total
number of extra syllables.

**Sweep values for FLAT_PENALTY:** [0 (current), 5,000, 10,000]

### Approach C: Fix tone-mismatch test cases (prerequisite)

Before sweeping, fix the 8 test cases that fail due to tone mismatches. These
pollute the multi_syllable metrics and hide the true effect of penalty changes.

**Two options:**
1. Fix the test cases to use the correct dictionary tone (man4, haa6, etc.)
2. Add the common tone variants to the dictionary (both man2 and man4 for 文)

Option 1 is faster but masks a real user experience issue. Option 2 is more principled
but requires dictionary changes.

**Recommended:** Fix test cases (option 1) for now, and separately investigate adding
tone variants as a future improvement.

### Approach D: Investigate tone-fuzzy matching (separate experiment)

The 8 tone-mismatch failures suggest a broader opportunity. Currently, tone matching
is exact: if the query specifies tone 2, only tone 2 matches. A tone-fuzzy mode could
treat wrong-tone matches as a penalty rather than a hard rejection.

This is a separate experiment from the unmatched penalty sweep, but could have a larger
impact on multi_syllable results (fixing 8/12 failures vs the 0-1 that the unmatched
penalty affects).

## Recommended Approach

**Three steps:**

1. **Fix test cases** (Approach C, option 1): Correct the 8 tone-mismatch test cases
   so multi_syllable metrics accurately reflect ranking quality, not jyutping coverage.

2. **Sweep UNMATCHED_JYUTPING_PENALTY** (Approach A): Test [10K, 15K, 20K, 25K]
   against the full test suite. This is a safe experiment since the constant only
   affects entries with unmatched positions.

3. **Optionally add flat penalty** (Approach B): If Approach A alone shows limited
   improvement, add a flat per-extra-syllable penalty as a secondary lever.

### Sweep parameters

1. `UNMATCHED_JYUTPING_PENALTY`: [10_000, 15_000, 20_000, 25_000]
2. Optional: `FLAT_EXTRA_SYLLABLE_PENALTY`: [0, 5_000, 10_000]

With Approach A only: 4 combinations.
With A+B: 4 × 3 = 12 combinations.

### Implementation steps

1. Fix 8 tone-mismatch test cases in `query_set.json`
2. Re-run eval to establish clean baseline for multi_syllable
3. Generate focused `eval/query_sets/shorter_entry.json` test set covering:
   - 2-syllable queries where both 2 and 3+ syllable entries exist
   - Queries where the 2-syllable entry has varying static_cost levels
   - Queries that should match longer entries (e.g., `nei5` → show 你好)
4. Run parameter sweep (only rebuilds search, no dictionary rebuild needed)
5. Analyze results per-category, especially multi_syllable and single_tone
6. Check for regressions in single_tone and partial_prefix categories

### Regression risk

Increasing the penalty could push some currently-correct longer entries too far down.
Categories to monitor:
- `single_tone`: Single-syllable queries match many multi-syllable entries. Higher
  unmatched penalty could change which longer entries appear.
- `partial_prefix`: Already the weakest category (72% p@1). Changes to unmatched
  penalty interact with the prefix match penalty.
- `cantonese_vocab`: Some Cantonese vocabulary entries are multi-syllable.

### Expected impact

**Honest assessment:** The impact on p@1 will be small because most multi_syllable
failures are tone mismatches, not penalty issues. The sweep may find that the current
value (10,000) is already near-optimal for the cases where it matters.

The larger opportunity is **tone-fuzzy matching** (Approach D), which could fix 8 of
the 12 multi_syllable failures. This should be written up as a separate experiment plan.

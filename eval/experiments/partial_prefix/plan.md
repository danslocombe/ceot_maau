# Experiment Plan: Partial Prefix Matching Improvement

## Problem

The `partial_prefix` category is the weakest non-edge category at **72% p@1** (0.83 MRR).
These are queries where the user hasn't finished typing a syllable, e.g., `ja` for 也 (jaa5),
`gon` for 講 (gong2), `daa` for 大 (daai6).

### How partial matching works today

When a query like `ja` is evaluated, search.rs tries three strategies for each jyutping
base string in the dictionary (lines 44-76):

1. **Exact match**: Query string equals base string → cost 0
2. **Substring match**: Query found inside base string at position `idx`
   ```
   cost = JYUTPING_NON_PERFECT_MATCH                    (6,000)
        + idx * JYUTPING_PARTIAL_MATCH_PENALTY_K         (idx × 12,000)
        + remaining * JYUTPING_COMPLETION_PENALTY_K       (remaining × 4,000)
   ```
3. **Prefix Levenshtein**: Edit distance < 2 → `6,000 + dist × 20,000`

For a prefix match (idx=0), the cost simplifies to:
```
cost = 6,000 + remaining_chars × 4,000
```

### Root cause: all prefix matches cost the same

For query `ja`, all of these get the same match cost of **10,000** (6,000 + 1×4,000):
- `jaa` (也, 丫, etc.) — remaining = 1
- `jan` (人, 因, etc.) — remaining = 1
- `jat` (一, 日, etc.) — remaining = 1
- `jau` (有, 又, etc.) — remaining = 1

Since all share the same match cost, the final ranking is determined entirely by
`static_cost` (character frequency). Common characters like 人 (jan4), 一 (jat1), 有 (jau5)
beat less-common targets like 也 (jaa5).

### Failure analysis

14 of 50 partial_prefix cases fail (position > 1):

| ID  | Query  | Expected      | Position | Why it loses |
|-----|--------|---------------|----------|-------------|
| 78  | `ja`   | 也 (jaa5)     | 4        | 人/一/有 are more frequent |
| 79  | `heoi` | 去 (heoi3)    | 2        | Another heoi- entry is cheaper |
| 80  | `gon`  | 講 (gong2)    | 3        | 港/工 are more frequent |
| 432 | `gin`  | 見 (gin3)     | 3        | Other gin- entries cheaper |
| 435 | `bei`  | 被 (bei6)     | 2        | 比 (bei2) cheaper |
| 436 | `daa`  | 大 (daai6)    | 6        | Many daa- entries cheaper |
| 439 | `maa`  | 馬 (maa5)     | 2        | 媽 (maa1) cheaper |
| 440 | `baa`  | 巴 (baa1)     | 7        | Many baa- entries cheaper |
| 447 | `hok`  | 學 (hok6)     | 2        | Another hok- entry cheaper |
| 456 | `fei`  | 妃 (fei1)     | 2        | 飛 (fei1) cheaper |
| 457 | `ceoi` | 催 (ceoi1)    | 2        | Another ceoi- entry cheaper |

Two patterns emerge:

1. **Frequency competition** (most cases): The expected character simply isn't the most
   frequent among all characters sharing the same prefix. These may be unreasonable
   test expectations — when a user types `ja`, it's ambiguous whether they want jaa/jan/jat/jau.

2. **Same-syllable competition** (bei, maa, hok, fei, ceoi): The expected character loses
   to another character with the exact same syllable but different tone/meaning. These
   are pure frequency ranking issues, not prefix-matching issues.

### Which failures are actionable?

The sweep should focus on cases where the penalty formula itself could be improved.
The key insight is that the current formula treats all "1 character remaining" matches
identically, whether the remaining character is a vowel extension (ja→jaa) or a
consonant (ja→jan). A smarter penalty might prefer closer phonetic matches.

However, this requires more than just constant tuning — it would need formula changes
to the matching logic itself.

## Proposed Approaches

### Approach A: Review and fix test cases

Before sweeping, audit whether the 14 failing test cases have reasonable expectations.
For queries like `ja` (ambiguous prefix matching 4+ different syllables), expecting a
specific character at position 1 may be unreasonable. Consider:
- Relaxing `accept_top_n` for ambiguous prefixes (e.g., 2-char prefixes matching many syllables)
- Removing test cases where the expected answer is clearly not the most common character

### Approach B: Sweep JYUTPING_COMPLETION_PENALTY_K

The completion penalty (currently 4,000) controls how much we penalize matches that
need more characters to complete. Reducing it makes partial matches cheaper overall;
increasing it penalizes them more.

**Sweep values:** [2,000, 4,000 (current), 6,000, 8,000]

**Impact of increasing to 8,000:**
- `ja` → `jaa` (1 remaining): cost goes from 10,000 to 14,000
- `ja` → `jan` (1 remaining): same increase
- No relative change between competing prefix matches with same remaining count

**Problem:** This constant doesn't help with the core issue because competing entries
have the same number of remaining characters. It mainly affects whether prefix matches
rank above or below exact matches from other syllables.

### Approach C: Sweep JYUTPING_NON_PERFECT_MATCH

This base penalty (currently 6,000) applies to ALL non-exact matches. Reducing it makes
partial matches relatively more competitive against exact matches from different syllables.

**Sweep values:** [3,000, 6,000 (current), 9,000]

**Note:** This was already swept in the exact_vs_prefix experiment. Current value (6,000)
was chosen for best overall metrics. Unlikely to change, but can re-verify with the new
test suite (745 cases vs 650).

### Approach D: Add vowel-consonant awareness to completion penalty

Currently, `remaining_chars` treats all characters equally. A smarter formula could
give a bonus when the query matches the full onset+nucleus (consonant+vowel core) of
the syllable, penalizing only coda (final consonant) completion:

```
// Pseudocode for smarter completion penalty
if query matches full vowel of syllable (e.g., "jaa" for "jaat"):
    completion_cost = remaining * COMPLETION_PENALTY_CODA  // smaller
else:
    completion_cost = remaining * COMPLETION_PENALTY_K     // current
```

This would require changes to the matching logic, not just constant tuning. It's a
more complex implementation but addresses the root cause.

### Approach E: Frequency-weighted completion bonus

Give prefix matches a bonus proportional to the entry's frequency. Common characters
that share a prefix with the query get a small discount:

```
completion_cost = remaining * COMPLETION_PENALTY_K - frequency_bonus
```

This is ad-hoc and risks overfitting but could address the frequency competition issue.

## Recommended Approach

**Two steps:**

1. **Audit test cases** (Approach A): Review the 14 failures and fix unreasonable
   expectations. Many partial_prefix queries are inherently ambiguous, and the "expected"
   answer is just one of several valid results. Increase `accept_top_n` for ambiguous
   cases or update expected characters to include the actual winner.

2. **2D sweep of COMPLETION_PENALTY_K × NON_PERFECT_MATCH** (Approaches B+C):
   Test [2K, 4K, 6K, 8K] × [3K, 6K, 9K] = 12 combinations. This is a search-only
   sweep (no dictionary rebuild). Monitor all categories for regressions, especially
   exact_vs_prefix which was tuned with NON_PERFECT_MATCH=6,000.

### Sweep parameters

- `JYUTPING_COMPLETION_PENALTY_K`: [2,000, 4,000, 6,000, 8,000]
- `JYUTPING_NON_PERFECT_MATCH`: [3,000, 6,000, 9,000]
- Total: 12 combinations, ~25s each = ~5 minutes

### Categories to monitor for regressions

- `exact_vs_prefix` (88% p@1): Previously optimized with current constants
- `single_tone` (97% p@1): Single-syllable exact matches
- `multi_syllable` (97% p@1): Multi-syllable matches with tone
- `shorter_entry` (100% p@1): Short vs long entry preference

### Expected impact

**Honest assessment:** The impact will likely be small. Most partial_prefix failures are
frequency competition where the expected character isn't the most common for that prefix.
Constant tuning can't fix this without also changing what wins for other queries.

The higher-impact path is Approach A (fixing test expectations) combined with Approach D
(smarter completion logic that understands Cantonese phonotactics). Approach D is a code
change, not a constant sweep, and should be a separate implementation task.

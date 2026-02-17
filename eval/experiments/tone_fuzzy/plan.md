# Experiment Plan: Tone-Fuzzy Matching

## Problem

When a user specifies a tone in their jyutping query, the search requires an **exact tone
match**. If the query says `man2` but the dictionary entry has `man4`, the entry is completely
rejected — no partial credit, no penalty-based ranking. The entry simply doesn't appear.

This causes real failures because Cantonese has common tone alternations that users
encounter frequently:

| User types | Dict has | Word | Tone relationship |
|------------|----------|------|-------------------|
| man**2** | man**4** | 文 (writing) | Changed tone (2↔4) |
| soeng**5** | soeng**6** | 上 (above) | Changed tone (5↔6) |
| haa**5** | haa**6** | 下 (below) | Changed tone (5↔6) |
| nin**2** | nin**4** | 年 (year) | Changed tone (2↔4) |
| ji**1** | ji**5** | 已 (already) | Different initial tone |
| guk**2** | guk**6** | 局 (bureau) | Changed tone (2↔6) |

These aren't typos — they represent legitimate Cantonese pronunciation variants (changed
tones, literary vs colloquial readings). We fixed the test cases to use dictionary tones,
but real users will type the "wrong" tone.

### How tone matching works today

In `search.rs` lines 324-336, the `matches_jyutping_term()` function:

```rust
if let Some(t) = jyutping_term.tone
{
    if t == entry_jyutping.tone    // Exact match only
    {
        term_match = true;
    }
}
else
{
    term_match = true;  // No tone specified → match any tone
}
```

The tone is stored as a `u8` (0-6) in the `Jyutping` struct. The query tone is parsed
by `jyutping_splitter::parse_jyutping_tone()` which extracts the trailing digit.

### Impact estimate

The 8 tone-mismatch cases we fixed in query_set.json represent the known failures.
But the actual impact is broader — any user who types a common but "wrong" tone for
any syllable will get no results for that syllable. With ~120,000 dictionary entries,
there are likely many entries with tone variants that users encounter.

## Proposed Approach

### Core change: treat tone mismatch as a penalty, not a rejection

Modify `matches_jyutping_term()` to accept tone-mismatched entries with an additional
penalty cost:

```rust
// New constant
pub const JYUTPING_TONE_MISMATCH_PENALTY: u32 = 8_000;

// Modified matching logic
if let Some(t) = jyutping_term.tone
{
    if t == entry_jyutping.tone
    {
        term_match = true;
        // tone_penalty = 0 (exact match)
    }
    else
    {
        term_match = true;
        tone_penalty = JYUTPING_TONE_MISMATCH_PENALTY;
    }
}
```

The `tone_penalty` is added to `term_match_cost` for that syllable, making tone-mismatched
entries rank below exact-tone matches but above "not found".

### Design decisions

**1. Flat penalty vs distance-based penalty**

Option A: Flat penalty — any tone mismatch gets the same cost.
Option B: Distance-based — `|query_tone - entry_tone| × PENALTY_PER_STEP`
Option C: Linguistically-aware — use a tone similarity matrix based on Cantonese
phonology (tones 2↔5, 3↔6 are closer than 1↔6).

**Recommendation:** Start with Option A (flat penalty). It's simplest to implement and
sweep. Cantonese tone relationships are complex and a flat penalty captures the main
benefit (finding results) without over-engineering the similarity metric.

**2. Penalty magnitude**

The penalty should be:
- **Large enough** that exact-tone matches always rank above tone-mismatched matches
- **Small enough** that tone-mismatched entries still appear in top-10 results

For reference, current cost components for a typical 2-character entry:
- `static_cost`: 12,000–25,000 (depends on character frequency)
- `term_match_cost` for exact prefix match: 6,000 (JYUTPING_NON_PERFECT_MATCH)
- `UNMATCHED_JYUTPING_PENALTY`: 10,000–30,000 per unmatched syllable

A tone mismatch penalty of 5,000–15,000 per syllable would put tone-mismatched entries
below exact-tone matches but likely still within the top-10.

**Sweep values:** [5,000, 8,000, 12,000, 16,000]

**3. Multi-syllable interaction**

For a 2-syllable query like `soeng5 min6` matching entry `soeng6 min6`:
- Syllable 1: tone mismatch → +PENALTY
- Syllable 2: exact match → +0
- Total tone penalty: 1 × PENALTY

For `jing1 man2` matching `jing1 man4`:
- Syllable 1: exact match → +0
- Syllable 2: tone mismatch → +PENALTY
- Total: 1 × PENALTY

This naturally handles partial tone mismatches — the more syllables that mismatch,
the higher the total penalty.

## Implementation

### Files to modify

| File | Change |
|------|--------|
| `dictlib/src/search.rs` | Add `JYUTPING_TONE_MISMATCH_PENALTY` constant. Modify `matches_jyutping_term()` to accept tone mismatches with penalty. |
| `dictlib/src/reconstruct_match.rs` | Update span highlighting to handle tone-mismatched entries (highlight the base match but not the tone digit). |

### Code change in search.rs

The change is localized to `matches_jyutping_term()` (lines 312-349). The function
currently sets `term_match = true` only on exact tone match. We modify it to also
accept mismatched tones with additional cost:

```rust
let mut tone_penalty: u32 = 0;
if let Some(t) = jyutping_term.tone
{
    if t == entry_jyutping.tone
    {
        term_match = true;
    }
    else
    {
        term_match = true;
        tone_penalty = JYUTPING_TONE_MISMATCH_PENALTY;
    }
}
else
{
    term_match = true;
}

// Later, when recording the match:
// total_term_match_cost += term_match_cost + tone_penalty;
```

### Span highlighting (reconstruct_match.rs)

Currently, the span reconstruction checks `if t == entry_jyutping.tone` to decide
whether to highlight the tone digit. For tone-mismatched entries, we should highlight
the base (consonant+vowel) but NOT the tone digit, giving the user visual feedback
that the tone differs.

## Test cases

### New query set: `eval/query_sets/tone_fuzzy.json`

Re-introduce the original "wrong tone" queries as a dedicated test set:

| Query | Expected | Note |
|-------|----------|------|
| jing1 man**2** | 英文 | Common variant: man2 for man4 |
| zung1 man**2** | 中文 | Common variant: man2 for man4 |
| soeng**5** min6 | 上面 | Common variant: soeng5 for soeng6 |
| haa**5** min6 | 下面 | Common variant: haa5 for haa6 |
| haa**5** ci3 | 下次 | Common variant: haa5 for haa6 |
| gam1 nin**2** | 今年 | Common variant: nin2 for nin4 |
| ji**1** ging1 | 已經 | Common variant: ji1 for ji5 |
| jau4 guk**2** | 郵局 | Common variant: guk2 for guk6 |

These should all have `accept_top_n: 3` since the tone-mismatched entry should appear
but may not be at position 1 (exact-tone matches should rank higher).

Also add **regression test cases** where tone-exact matching must still work:

| Query | Expected | Note |
|-------|----------|------|
| nei5 hou2 | 你好 | Exact tone — should still be p@1 |
| m4 hou2 | 唔好 | Exact tone — should still be p@1 |
| sik6 faan6 | 食飯 | Exact tone — should still be p@1 |

And **negative cases** where wrong tone should NOT promote unrelated entries:

| Query | Expected | Note |
|-------|----------|------|
| nei5 | 你 | Should not be beaten by 泥 (nei4) due to tone fuzzy |
| gam1 | 今 | Should not be beaten by 錦 (gam2) due to tone fuzzy |

## Sweep design

### Parameters
- `JYUTPING_TONE_MISMATCH_PENALTY`: [5,000, 8,000, 12,000, 16,000]
- No dictionary rebuild needed (search-only constant)
- 4 combinations, ~25s each = ~2 minutes

### Evaluation
- Full test suite (745+ cases) plus new tone_fuzzy test cases
- Primary metric: tone_fuzzy category p@1 and p@3
- Regression monitoring: all other categories, especially single_tone and multi_syllable
  where exact-tone matches must remain dominant

### Expected impact

**Optimistic:** All 8 tone-mismatch cases appear in top-3, gaining ~8 previously
"invisible" results with no regressions.

**Risk:** Tone-mismatched entries could crowd out correct entries in some edge cases.
For example, if a user types `nei5` and there exists an entry with `nei4`, the nei4
entry might now appear in results where it previously wouldn't. With a penalty of
8,000+, exact-tone matches should always win, but the top-10 list might shift.

## Alternatives considered

### Tone group matching
Define tone groups (e.g., {2,5}, {3,6}, {1,4}) and only apply fuzzy matching within
groups. More linguistically principled but adds complexity and may miss some cases.

### Dictionary-level tone variants
Add duplicate entries with common tone variants directly into the dictionary during
the build step. More reliable but inflates the dictionary and is harder to maintain.

### Lazy tone (strip all tones)
If tone-fuzzy is enabled, treat all queries as toneless. Too aggressive — loses the
valuable signal that tone provides for disambiguation.

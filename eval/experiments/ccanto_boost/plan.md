# Experiment Plan: CCanto Frequency Boost

## Problem

Cantonese-specific characters are systematically penalized by the static_cost system because
the frequency data (`full/frequencies.txt`) is derived from **Mandarin** text corpora
(Jun Da's Chinese Character Frequency List, 2004). Characters that are extremely common in
spoken/written Cantonese but rare or absent in Mandarin get the maximum penalty.

### Root cause

The cost formula is: `static_cost = sum(-1000 * ln(frequency))` per character, clamped to
`[1, 7000]`. Characters not in the frequency file get `MAX_STATIC_COST = 7000` per character.

**13 of 15 core Cantonese-specific characters are missing from the frequency file:**

| Character | Jyutping | Meaning | In freq file? | Cost per char |
|-----------|----------|---------|---------------|---------------|
| 嘅 | ge3 | possessive particle | No | 7,000 |
| 啲 | di1 | some/a bit | No | 7,000 |
| 佢 | keoi5 | he/she/it | No | 7,000 |
| 嘢 | je5 | thing/stuff | No | 7,000 |
| 嗰 | go2 | that | No | 7,000 |
| 冇 | mou5 | don't have | No | 7,000 |
| 係 | hai6 | to be | No | 7,000 |
| 喺 | hai2 | at/in | No | 7,000 |
| 噉 | gam2 | like this | No | 7,000 |
| 咁 | gam3 | so/such | No | 7,000 |
| 攞 | lo2 | to take | No | 7,000 |
| 嚟 | lai4 | to come | No | 7,000 |
| 揾 | wan2 | to find | No | 7,000 |
| 畀 | bei2 | to give | Yes | ~3,500 |
| 睇 | tai2 | to look | Yes | ~5,000 |

This means a single-character CCanto entry like 佢 gets `static_cost = 7000 + definition_heuristics`.
Meanwhile, a CEDict character like 拒 (refuse) gets `static_cost = 7000` too, but common Mandarin
characters like 道 get much lower costs (~4000-5000). The result: CCanto entries are at a
systematic disadvantage.

### Observed impact

From the eval:
- CCanto appears as top result in only **167/650** queries vs CEDict at **477/650**
- `keoi5` (佢, "he/she"): ranked **3rd** behind 拒 and 距 (both CEDict, static_cost 14,000
  vs 佢's 21,000). The 7,000 gap comes from the additional `cost_heuristic` penalties on
  the CCanto entry since its definitions don't contain "M:" or "CL:" markers.
- `gwaai3` (乖, "well-behaved"): doesn't appear in top 5 at all

### Why CEDict entries also get 7,000 per character but still win

Many CEDict characters have simplified/traditional forms that ARE in the Mandarin frequency
file (e.g. 怪 rank 775, 道 rank ~200). The frequency file contains a mix of traditional and
simplified forms (9,933 characters total), and common Mandarin characters in traditional form
are often present. CEDict characters also exist in both dictionaries (annotated with jyutping
later), so they benefit from lower base costs.

## Simplified-to-Traditional Frequency Lookup

### Investigation

Both `cedict_ts.u8` and `cccanto-webdist.txt` contain `Traditional Simplified` as the
first two columns of every entry. The builder currently parses the simplified form but
discards it (`_simplified`).

The Mandarin frequency file uses a mix of simplified and traditional characters (9,933
total). Many traditional characters (e.g. 機, 國, 學, 個) are absent but their simplified
equivalents (机, 国, 学, 个) are present.

**Analysis results:**
- 3,705 traditional characters have a different simplified form in the dictionary data
- **2,162** of these are missing from the frequency file but their simplified form IS present
- This is a large, completely free improvement — these characters currently all get
  `MAX_STATIC_COST = 7,000` but could get proper frequency-based costs

**Example savings per character:**

| Traditional | Simplified | Current cost | With simp lookup | Saving |
|-------------|-----------|-------------|-----------------|--------|
| 國 | 国 | 7,000 | 5,280 | 1,720 |
| 個 | 个 | 7,000 | 5,083 | 1,917 |
| 學 | 学 | 7,000 | 6,032 | 968 |
| 機 | 机 | 7,000 | 6,344 | 656 |

### Limitation: Does NOT fix Cantonese-specific characters

The trad→simp mapping doesn't help the core Cantonese characters because they have no
Mandarin equivalent at all:

| Character | Simplified mapping | In freq file? |
|-----------|--------------------|---------------|
| 冇 | no mapping | N/A |
| 喺 | no mapping | N/A |
| 啲 | no mapping | N/A |
| 嘢 | no mapping | N/A |
| 咁 | no mapping | N/A |
| 攞 | no mapping | N/A |
| 嚟 | no mapping | N/A |
| 揾 | no mapping | N/A |
| 佢 | 渠 (spurious) | No |
| 嘅 | 慨 (spurious) | No |
| 係 | 系 | Yes, but cost=6,921 (only 79 saving) |

Some mappings (佢→渠, 嘅→慨) are present in the dictionary data but are semantically
incorrect — 佢 is not the traditional form of 渠, it's a Cantonese-specific character.

## Proposed Approaches

### Approach 0: Simplified frequency fallback (prerequisite, no sweep needed)

Use the trad→simp mapping already present in the dictionary files to look up frequency
data for traditional characters whose simplified form exists in the frequency file.

**Implementation in `builder.rs`:**
1. During `parse_cedict()` and `parse_ccanto()`, also parse the simplified column
   (currently discarded as `_simplified`)
2. In `TraditionalToFrequencies`, add a `get_with_simplified_fallback(trad, simp)` method
   that checks the traditional character first, falls back to simplified if not found
3. Use this during cost computation for both CCanto and CEDict entries

**Impact:** Improves costs for 2,162 traditional characters across both sources.
No tuning needed — this is strictly correct. Apply first, then re-baseline.

### Approach A: CCanto source discount

Apply a flat cost reduction to all CCanto-sourced entries during build.

**Implementation:**
- In `builder.rs` `parse_ccanto()`, after computing cost, subtract a fixed amount:
  `cost = cost.saturating_sub(CCANTO_DISCOUNT)`
- Constant: `CCANTO_DISCOUNT = 3_000` (start value, tune via sweep)

**Pros:** One-line change, easy to sweep
**Cons:** Blunt instrument — helps all CCanto entries equally regardless of actual frequency

### Approach B: Cantonese frequency data (most principled)

Create or source a Cantonese character frequency file and use it for CCanto entries.

**Sources for Cantonese frequency data:**
- LIVAC (Linguistic Variation in Chinese Speech Communities) corpus
- Hong Kong Cantonese Corpus (HKCanCor)
- Words.hk frequency data
- Manually assign costs based on known Cantonese usage tiers

**Pros:** Most accurate, fixes the root cause
**Cons:** Requires sourcing/creating frequency data, more complex

### Approach C: Override costs for known high-frequency Cantonese characters

Hardcode cost overrides for the ~10 most common Cantonese-only characters that have
no simplified equivalent and no frequency data at all.

**Implementation:**
- Create a `CANTO_CHAR_COSTS` lookup in `builder.rs`
- Apply during cost computation: if character is in the override map, use the override
  cost instead of the frequency file cost
- Assign costs based on estimated Cantonese frequency tiers:
  - Tier 1 (嘅, 佢, 係, 冇, 喺, 咁, 嗰, 啲): cost = 1,000-2,000
  - Tier 2 (嘢, 噉, 攞, 嚟, 揾, 畀): cost = 2,000-3,000

**Pros:** Precise control, targets the exact problem
**Cons:** Requires manual curation, doesn't scale

### Approach D: Definition-based "(Cantonese)" bonus (already partially exists)

The existing heuristic `DoesNotContainTerms(&["(Cantonese)"]), 2_000` already gives a
2,000 cost bonus to entries whose definition contains "(Cantonese)". This could be increased.

**Pros:** Zero new infrastructure
**Cons:** Only helps entries that have "(Cantonese)" in their definition text

## Recommended Approach

**Three layers, applied in order:**

1. **Approach 0 (simplified fallback)** — Apply first as a prerequisite. Fixes 2,162
   traditional characters across both sources. No tuning needed. Re-baseline after.

2. **Approach C (Cantonese character overrides)** — Hardcode costs for the ~10-15
   Cantonese-specific characters that have no simplified equivalent and no frequency data.
   These are the highest-impact characters (佢, 嘅, 冇, 係, etc.).

3. **Approach A (CCanto source discount)** — If layers 1+2 aren't sufficient, add a
   small flat discount for CCanto entries to give them a general edge. Sweep to find
   the right value.

### Sweep parameters (for layers 2+3)

1. `CANTO_HIGH_FREQ_COST` (cost for tier-1 Cantonese chars): [1_000, 2_000, 3_000]
2. `CCANTO_DISCOUNT`: [0, 1_000, 2_000, 3_000]

This gives 12 combinations.

### Implementation steps

1. Implement Approach 0 (simplified fallback) in `builder.rs`
   - Parse simplified column in `parse_cedict()` and `parse_ccanto()`
   - Build a `trad_to_simp` map during dictionary parsing
   - Add fallback in `TraditionalToFrequencies::get_or_default()`
2. Rebuild dictionary index (`console.exe build`)
3. Run eval, save as new baseline
4. Implement Approach C (Cantonese character cost overrides)
5. Implement Approach A (CCanto discount constant)
6. Generate focused `eval/query_sets/ccanto_boost.json` test set covering:
   - Common Cantonese pronouns (佢 keoi5, 我 ngo5, 你 nei5)
   - Cantonese particles (嘅 ge3, 啲 di1, 嗰 go2, 咁 gam3, 噉 gam2, 喺 hai2)
   - Common Cantonese verbs (冇 mou5, 係 hai6, 攞 lo2, 嚟 lai4, 揾 wan2, 畀 bei2, 睇 tai2)
   - Multi-char Cantonese words (唔好 m4 hou2, 點解 dim2 gaai2, 乜嘢 mat1 je5)
7. Run parameter sweep
8. Analyze results, choose values, write findings

### Risk: Over-boosting CCanto

Monitor for regressions in:
- `single_tone` and `single_no_tone` categories
- `english` category (should be unaffected)
- Overall `not_found` count
- Cases where CEDict has the genuinely better entry

The sweep grid includes 0 discount as a control to detect regressions.

# Parameter Sweep: CCanto Frequency Boost

Date: 2026-02-17

## Background

Cantonese-specific characters are systematically penalized because the frequency data
(`full/frequencies.txt`) is derived from Mandarin text corpora. Characters extremely common
in Cantonese but rare/absent in Mandarin get `MAX_STATIC_COST = 7,000` per character.

Three changes were implemented:
1. **Simplified frequency fallback**: Use trad→simp mapping from dictionary files to look
   up frequency data for traditional characters whose simplified form exists in the file
2. **Cantonese character cost overrides**: Explicit costs for 13 Cantonese-specific characters
   with no Mandarin equivalent (佢, 嘅, 係, 冇, 喺, 咁, 嗰, 啲, 嘢, 噉, 攞, 嚟, 揾)
3. **CCanto source discount**: Flat cost reduction for all CCanto-sourced entries

## Constants Tuned

Two constants in `dictlib/src/builder.rs`:

- **`CANTO_HIGH_FREQ_COST`**: Per-character cost for tier-1 Cantonese characters.
  Tier-2 characters get `CANTO_HIGH_FREQ_COST + 1,000`.
- **`CCANTO_DISCOUNT`**: Flat cost subtracted from all CCanto entries after computing
  frequency-based cost + heuristics.

## Methodology

- 720 test cases (650 from `query_set.json` + 40 `exact_vs_prefix_extended.json` + 30 `ccanto_boost.json`)
- 30 test cases specifically for `ccanto_boost` category
- Swept 4 values of `CANTO_HIGH_FREQ_COST` × 4 values of `CCANTO_DISCOUNT` = 16 combinations
- Each combination: patch builder.rs, `cargo build --release`, rebuild dictionary, run full eval
- Total sweep time: ~6 minutes

## Results

```
    CC     CD | All p@1 All p@3 All MRR Miss | CCB p@1 CCB p@3 CCB MRR Miss
------ -------+------------------------------+-----------------------------
  1000      0 |     92%     97%    0.94   18 |     87%     93%    0.90    0  <- chosen
  1000   1000 |     91%     96%    0.94   19 |     90%     97%    0.93    0
  1000   2000 |     92%     96%    0.94   19 |     90%     97%    0.93    0
  1000   3000 |     91%     96%    0.94   19 |     90%     97%    0.94    0
  2000      0 |     92%     97%    0.94   18 |     87%     90%    0.90    0
  2000   1000 |     91%     96%    0.94   19 |     90%     97%    0.93    0
  2000   2000 |     92%     96%    0.94   19 |     90%     97%    0.93    0
  2000   3000 |     92%     96%    0.94   19 |     90%     97%    0.93    0
  3000      0 |     92%     97%    0.94   18 |     87%     90%    0.90    0
  3000   1000 |     92%     96%    0.94   19 |     90%     93%    0.93    0
  3000   2000 |     92%     96%    0.94   19 |     90%     97%    0.93    0
  3000   3000 |     92%     96%    0.94   19 |     90%     97%    0.93    0
  4000      0 |     92%     97%    0.94   18 |     87%     90%    0.90    0
  4000   1000 |     92%     96%    0.94   19 |     90%     93%    0.93    0
  4000   2000 |     92%     96%    0.94   19 |     90%     93%    0.93    0
  4000   3000 |     92%     96%    0.94   19 |     90%     97%    0.93    0
```

## Analysis

1. **Simplified fallback was the biggest single improvement.** Adding 2,164 frequency
   fallbacks (2,138 from CEDict + 26 from CCanto) reduced not-found from 22 to 18 and
   improved overall metrics before any Cantonese-specific tuning.

2. **CANTO_HIGH_FREQ_COST = 1,000 is optimal.** Lower character cost consistently
   produces best CCB p@3 (93% vs 90% at higher values). The effect on overall metrics
   is minimal since only 13 characters are affected.

3. **CCANTO_DISCOUNT has a consistent tradeoff.** Any discount > 0 improves CCB p@1
   from 87% to 90% but adds 1 overall miss (18→19). This happens because cheaper CCanto
   entries crowd out CEDict entries that are the correct answer for some queries.

4. **Zero not-found in CCanto category.** All 30 CCanto test cases now appear in top-10
   results across all parameter combinations. The character cost overrides eliminated all
   "missing" entries.

5. **Test case bugs discovered.** The initial sweep showed zero variation because
   `expected_characters` in ccanto_boost.json used strings instead of lists. The
   `_match_result` function iterates over the value, so strings were compared character-
   by-character against multi-character results. Also found: wrong tone (gwaai3→gwaai1),
   wrong character form (揾→搵 traditional), and missing dictionary entries (喺 standalone,
   睇嘢 compound).

## Decision

**Chosen values: `CANTO_HIGH_FREQ_COST = 1,000`, `CCANTO_DISCOUNT = 0`**

Rationale:
- Best overall p@1 (92%) tied with several others
- Best overall p@3 (97%) — only CD=0 achieves this
- Lowest not-found count (18)
- CCB p@1 at 87% with p@3 at 93% — strong for a targeted category
- No discount avoids the regression risk of over-boosting CCanto entries

## Cumulative Impact (from original baseline)

| Metric | Original | After exact/prefix sweep | After CCanto boost | Total delta |
|--------|----------|--------------------------|---------------------|-------------|
| Overall p@1 | 88% | 92% | 92% | +4% |
| Overall p@3 | 94% | 96% | 97% | +3% |
| Overall MRR | 0.91 | 0.94 | 0.94 | +0.03 |
| Not found | 22 | 18 | 18 | -4 |
| CCB p@1 | n/a | n/a | 87% | new |
| CCB p@3 | n/a | n/a | 93% | new |

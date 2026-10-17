# Experiment: annotation provenance (exact readings + native preference)

Status: **run** — hypothesis denied; exact annotation kept, native-preference dropped.
See `findings.md`.

## Hypothesis

Assigning a Cantonese reading to a derived (CEDict) entry **only when the
readings table attests the exact `(traditional, pinyin)` pair**, and
**preferring native (CC-Canto) entries over derived ones**, improves search
relevance on the eval suite — and, separately, removes entries/glosses that are
not really Cantonese.

Alternative: the pair is neutral on the eval suite (which scores character
position) and only changes *which gloss* is shown, which the suite cannot see.

## Background

`build_for_github_pages`-time pipeline currently:

1. `parse_cedict` reads CEDict (Mandarin) entries with no Cantonese reading.
2. `TraditionalToJyutping::parse` collapses the readings file
   (`trad simp [pinyin] {jyutping}`) to **`traditional -> [jyutping]`**, dropping
   the pinyin.
3. `annotate` looks up the entry's **traditional form only** and assigns the
   first reading. Any CEDict entry whose traditional form is in the table gets a
   reading — including senses the table never claimed.

Consequences observed:

- `個` has two CEDict entries, Mandarin `ge3` ("used in 自個兒") and `ge4`
  ("classifier …"). The table lists `個 个 [ge4] {go3}`. Both get `go3`, so the
  Mandarin-only `ge3` sense surfaces as a Cantonese result for `go3`.
- 1,634 derived entries get a reading their pinyin does not attest.
- A bogus CC-Canto line (`嗰 {go3}`; the word is `go2`) plus the ranking
  heuristics make `嗰` the top hit for `go3` over the far more common `個`.

### Exposure of the eval suite

Counting `expected_characters` occurrences across all 3,003 cases:

| bucket | occurrences | how the change touches it |
|---|---:|---|
| native only (CC-Canto) | 806 | native pref: reorders only |
| native **and** derived | 1,125 | native pref: picks which one represents the char |
| derived, attested `(form,pinyin)` | 1,601 | pinyin-exact: kept → neutral |
| derived, **fabricated** | 28 | pinyin-exact: **dropped** → possible regression |
| absent from both | 14 | — |

**Important:** `run_eval._match_result` matches on `expected_characters`, so the
suite measures whether the expected character appears and at what position. It
is **blind to gloss quality** — the `自個兒` junk scores the same as a good gloss
if the characters match. So we should expect, at best, modest movement, and we
must check gloss quality ad hoc.

## Changes under test (arms)

Two independent toggles:

- **A — exact annotation**: `annotate` matches `(traditional, pinyin)`
  (normalised: strip spaces, lowercase, `ü`/`u:`) and leaves the reading empty
  on no match. Build-time: needs an index rebuild.
- **B — native preference**: `Native` (CC-Canto) entries rank ahead of `Derived`
  (CEDict) ones. Cheapest form for the experiment: add a cost offset in
  `parse_cedict` / set `CCANTO_DISCOUNT > 0`. Build-time: also needs a rebuild.

Dedup (`DEDUPE_BY_CHARACTER`) is orthogonal; keep it **on** for isolating A/B,
then test it as a separate arm.

Arms:

| arm | annotate | native pref | dedup |
|---|---|---|---|
| baseline | current (form-only) | off (`CCANTO_DISCOUNT=0`) | on |
| A | exact | off | on |
| B | exact | on | on |
| B-noDedup | exact | on | off |

## Method

1. Build the release console. Save the baseline index; build the treatment index.
2. For each arm: `python eval/run_suite_report.py --save eval/results/<arm>.json`.
3. `python eval/run_suite_report.py --compare baseline.json <arm>.json`.
4. Ad-hoc (not scored by the suite): `go3`, `go2`, `lou5 si1`, 老師, 行, 長 —
   look at *which gloss* is shown, not just position.

## Expected outcome

- p@1/MRR roughly flat: A can only drop the 28 fabricated expected chars
  (regressions) and remove fabricated distractors (improvements); B can only
  reorder the 1,125 native+derived expected chars.
- The real, checkable gain is qualitative: `go3` should stop showing
  "used in 自個兒…", and `個` should show CC-Canto's classifier gloss.
- **嗰 is still likely #1 for `go3`** — it is native and cheap; the pair does not
  touch the tier-1 `(Cantonese)` heuristics or the bogus CC-Canto line. This is
  a separate experiment.

## Decision criteria

- If p@1/MRR move ≥ ~0.5pp positive with no set regressing ≫ that, keep.
- If the suite is flat (expected), decide on the qualitative result: does the
  change remove clearly-wrong entries without losing reachable ones?
- Any regression must be inspected case-by-case (are the dropped 28 expected
  chars actually correct Cantonese?).

# Findings: annotation provenance

Status: **run**. Hypothesis **denied as stated**, with a useful correction.

## Result

3003 cases, 9 sets. Release console, index format v10.

| arm | p@1 | p@3 | miss | MRR |
|---|---:|---:|---:|---:|
| **baseline** (form-only annotate, no penalty) | **92.4%** | 98.0% | 0.7% | **0.952** |
| exact annotate, normaliser v1 (`u:`→`ü` only) | 91.7% | 97.2% | 1.6% | 0.945 |
| exact annotate, normaliser v2 (+ `v`→`ü`, tone 5→4) | 92.3% | 98.0% | 0.8% | 0.952 |
| exact annotate v1 + derived penalty 3000 | 91.4% | 96.8% | 1.6% | 0.943 |
| exact annotate v2 + derived penalty 3000 | 92.1% | 97.6% | 0.8% | 0.950 |

So:

- **Exact annotation is ~neutral** once pinyin normalisation is fixed
  (−0.0pp p@1, net −1 case). It is *safe*, and it does remove the fabricated
  entries. It is not a ranking win.
- **The global derived penalty is harmful** (−0.2pp on top of exact, and it is
  what caused the −1.0pp in the first combined run). `water → 水` fell from
  position 2 → out of the top 10, `big → 大` from 2 → 10.

## Why the hypothesis failed

1. **The suite is blind to what we were fixing.** `run_eval._match_result`
   matches on `expected_characters`. The `個` "used in 自個兒…" gloss and a good
   CC-Canto gloss score identically. So removing bad glosses cannot show up as
   p@1.
2. **Most correct answers are derived.** ~78% of entries are CEDict. Of the
   expected-character occurrences, 1,601 are derived-attested-only. A blanket
   `DERIVED_COST_PENALTY` demotes those too, so it hurts far more than it helps.
3. **Exact matching was initially too strict**, not wrong. CEDict writes `lu:4`
   and the readings table `lv4`; CEDict `xia4 mian4` vs table `xia4 mian5`.
   Matching on the raw string dropped legitimate words (下面, 笑話, 旅行, 法律,
   綠 …). Normalising ü spellings and folding neutral tone 5→4 recovers them
   while still dropping the genuinely different `個 ge3`/`ge4`.

## Ad-hoc (qualitative — the actual point of the change)

- `go3`, exact annotate: the CEDict `個 ge3` entry loses its reading, so
  "used in 自個兒…" no longer appears. `個` shows CC-Canto's
  "classifier for people or objects in general…".
- **`嗰` is still #1 for `go3`** — it is native, cheap (tier-1 cost), and has a
  bogus `{go3}` line. Untouched by this change, as predicted.

## Correction

The native preference should be **per-character**, not global: prefer the native
entry only when a native entry exists for the *same* character (i.e. in the
per-character dedup / selection), leaving derived-only answers untouched. That
is the untested variant and the one that could show a real (if small) p@1 gain.

## Recommended state

- Keep **exact annotation** (normaliser v2): behaviour-neutral on the suite,
  removes fabricated entries/glosses.
- Drop the **global `DERIVED_COST_PENALTY`** (set back to 0).
- Retest a **per-character** native preference separately.
- Ranking (tier-1 cost / `(Cantonese)` penalty) and the `嗰 {go3}` data line
  remain separate, unsolved here.

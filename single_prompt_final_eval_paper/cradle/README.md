# CRADLE Bench (clean_active)

- **Dataset**: `SungJoo/Cradle-Bench`,
  revision `7007ba1d1bd0eecff6c872fd99e189cef1ef1e20`.
- **Split**: `test` (600 rows), text cleaned of title/prefix/boilerplate
  (`scripts/cradle_extract_testset.py`), filtered to the 401-row self-harm
  subset (`scripts/cradle_build_self_harm_subset.py`).
- **Subset** (`clean_active`; 304 prompts: 186 safe / 118 unsafe): keep
  `no_crisis` rows plus rows with at least one of
  `{selfharm_ongoing, suicideideation_active_ongoing}`.
  Exact rows in `subset.jsonl`.
- **Label mapping** (`ongoing_active` rule): `unsafe` iff any `_ongoing` tag
  except `suicideideation_passive_ongoing`; `safe` otherwise.

## Confusion matrices `[[TN, FP], [FN, TP]]` (positive class: unsafe)

- Classifier: `[[172, 14], [13, 105]]`
- Classifier + pass-gate: `[[175, 11], [14, 104]]`

Full metrics with 95% BCa bootstrap CIs (10,000 resamples, paired, seed 42)
in `metrics.json`.

## Files

- `subset.jsonl` — test set (`question_id`, `prompt`, `label`, `source_category`).
- `classifier.jsonl` — classifier predictions.
- `classifier_pg.jsonl` — classifier + pass-gate predictions (`final_unsafe`).
- `metrics.json` — metrics, CIs, confusion matrices.

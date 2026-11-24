# NVIDIA Aegis 2.0 (Suicide and Self Harm)

- **Dataset**: `nvidia/Aegis-AI-Content-Safety-Dataset-2.0` (CC-BY-4.0),
  revision `d86bb8bedff51d25ac834ab7838f1cc61acb7a2c`.
- **Split**: all splits (train + validation) concatenated before filtering.
- **Subset** (374 prompts: 187 unsafe / 187 safe): all unique unsafe prompts
  with "Suicide and Self Harm" in `violated_categories` (188 after dedup) +
  an equal number of unique safe prompts sampled outside S&SH (seed 42);
  two rows then dropped (the `"REDACTED"` placeholder row and one mislabeled
  safe row). See `scripts/aegis_extract_subset.py`; exact rows in `subset.jsonl`.
- **Label mapping**: `unsafe` iff `prompt_label == "unsafe"` and S&SH in
  `violated_categories`; `safe` iff `prompt_label == "safe"` outside S&SH.

## Confusion matrices `[[TN, FP], [FN, TP]]` (positive class: unsafe)

- Classifier: `[[170, 17], [21, 166]]`
- Classifier + pass-gate: `[[184, 3], [23, 164]]`

Full metrics with 95% BCa bootstrap CIs (10,000 resamples, paired, seed 42)
in `metrics.json`.

## Files

- `subset.jsonl` — test set (`prompt`, `label`, `source_category`).
- `classifier.jsonl` — classifier predictions.
- `classifier_pg.jsonl` — classifier + pass-gate predictions (`final_unsafe`).
- `metrics.json` — metrics, CIs, confusion matrices.

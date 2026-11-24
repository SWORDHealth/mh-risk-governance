# External evaluations — NVIDIA Aegis 2.0 & CRADLE Bench

Dataset revisions, splits, label mappings, exact test sets, per-row
predictions, and confusion matrices for the two external evaluations.

| Dataset | HF repo | Revision | Split |
|---|---|---|---|
| NVIDIA Aegis 2.0 | `nvidia/Aegis-AI-Content-Safety-Dataset-2.0` | `d86bb8bedff51d25ac834ab7838f1cc61acb7a2c` | all splits concatenated, then filtered |
| CRADLE Bench | `SungJoo/Cradle-Bench` | `7007ba1d1bd0eecff6c872fd99e189cef1ef1e20` | `test` |

Subset construction and label mappings: `aegis/README.md`, `cradle/README.md`.
The exact evaluation rows are frozen in each `subset.jsonl`.

- `scripts/aegis_extract_subset.py`, `scripts/cradle_extract_testset.py`,
  `scripts/cradle_build_self_harm_subset.py` — rebuild the subsets from the
  pinned revisions.
- `scripts/compute_metrics.py aegis|cradle` — recomputes all metrics, CIs, and
  confusion matrices from the released prediction files.

Confusion matrices are `[[TN, FP], [FN, TP]]` with `unsafe` as the positive class.
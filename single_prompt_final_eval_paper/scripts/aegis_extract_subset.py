#!/usr/bin/env python3
"""Extract the balanced Aegis 2.0 S&SH subset: all unique unsafe "Suicide and
Self Harm" prompts + an equal number of safe prompts sampled outside S&SH."""

import argparse
from pathlib import Path

import pandas as pd
from datasets import concatenate_datasets, load_dataset

SH_TAG = "Suicide and Self Harm"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seed", type=int, default=42, help="Random seed for safe sampling")
    ap.add_argument("--output", default="outputs/aegis2_self_harm_balanced.jsonl")
    args = ap.parse_args()

    print("Loading nvidia/Aegis-AI-Content-Safety-Dataset-2.0 ...")
    ds = load_dataset("nvidia/Aegis-AI-Content-Safety-Dataset-2.0")
    df = concatenate_datasets(list(ds.values())).to_pandas()
    df["cat"] = df["violated_categories"].fillna("")
    print(f"  total rows: {len(df)}")

    sh = df[df["cat"].str.contains(SH_TAG)].copy()
    sh_unsafe = sh[sh["prompt_label"] == "unsafe"]
    sh_unsafe_dedup = sh_unsafe.drop_duplicates("prompt")
    n_unsafe = len(sh_unsafe_dedup)
    print(f"  unique unsafe '{SH_TAG}' prompts: {n_unsafe}")

    safe_pool = df[(df["prompt_label"] == "safe") & (~df["cat"].str.contains(SH_TAG))]
    safe_dedup = safe_pool.drop_duplicates("prompt")
    print(f"  unique safe prompts (outside S&SH): {len(safe_dedup)}")

    safe_sample = safe_dedup.sample(n=n_unsafe, random_state=args.seed)
    print(f"  sampled safe prompts: {len(safe_sample)}")

    unsafe_out = sh_unsafe_dedup[["prompt", "prompt_label", "cat"]].copy()
    unsafe_out = unsafe_out.rename(columns={"cat": "source_category", "prompt_label": "label"})

    safe_out = safe_sample[["prompt", "prompt_label", "cat"]].copy()
    safe_out = safe_out.rename(columns={"cat": "source_category", "prompt_label": "label"})

    combined = pd.concat([unsafe_out, safe_out], ignore_index=True)
    print(f"\n  final dataset: {len(combined)} rows")
    print(f"  label counts: {combined['label'].value_counts().to_dict()}")

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    combined.to_json(out_path, orient="records", lines=True)
    print(f"  saved: {out_path}")


if __name__ == "__main__":
    main()

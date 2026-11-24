#!/usr/bin/env python3
"""Extract the SungJoo/Cradle-Bench test split as JSONL (question_id, prompt,
final_labels), cleaning title/prefix/boilerplate from question_text."""

import argparse
import re
from pathlib import Path

from datasets import load_dataset


def clean_text(text: str) -> str:
    idx = text.find("For any crisis present")
    if idx != -1:
        text = text[:idx]

    text_idx = text.find("Text:")
    if text_idx != -1:
        text = text[text_idx + len("Text:"):]

    return text.strip()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="outputs/cradle_bench_test.jsonl")
    args = ap.parse_args()

    ds = load_dataset("SungJoo/Cradle-Bench")
    test = ds["test"]

    rows = []
    for row in test:
        rows.append({
            "question_id": row["question_id"],
            "prompt": clean_text(row["question_text"]),
            "final_labels": row["final_labels"],
        })

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        import json
        for r in rows:
            f.write(json.dumps(r) + "\n")

    print(f"Saved {len(rows)} rows to {out_path}")
    print("\nSample (first row):")
    print(f"  question_id: {rows[0]['question_id']}")
    print(f"  final_labels: {rows[0]['final_labels']}")
    print(f"  prompt (first 400 chars):")
    print(f"    {rows[0]['prompt'][:400]}")


if __name__ == "__main__":
    main()

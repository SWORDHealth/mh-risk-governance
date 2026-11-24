#!/usr/bin/env python3
"""Filter the CRADLE Bench test JSONL to the self-harm subset: keep rows tagged
`no_crisis` or with a selfharm/suicideideation tag, excluding violence/abuse rows."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

VIOLENCE_STEMS = ("rape_", "sexualharassment_", "domesticviolence_", "childabuse_")


def is_self_harm_or_safe(labels: str) -> bool:
    tags = [t.strip() for t in (labels or "").split(",") if t.strip()]
    if not tags or tags == ["no_crisis"]:
        return True
    if any(any(t.startswith(stem) for stem in VIOLENCE_STEMS) for t in tags):
        return False
    return any(("selfharm" in t) or ("suicideideation" in t) for t in tags)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", default="cradle_bench_test.jsonl")
    ap.add_argument("--output", default="cradle_bench_self_harm.jsonl")
    args = ap.parse_args()

    kept = []
    with open(args.input) as f:
        for line in f:
            d = json.loads(line)
            if is_self_harm_or_safe(d["final_labels"]):
                kept.append(d)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        for d in kept:
            f.write(json.dumps(d) + "\n")
    print(f"Wrote {len(kept)} rows to {out}")


if __name__ == "__main__":
    main()
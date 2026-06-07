"""
Build train/val/test splits of the main FormatBench dataset.

Stratifies by `context` so each split has representative coverage of all
categories. Uses a fixed seed for reproducibility. Saves three JSONL files
in data/splits/.

Split ratio: 80% train / 10% val / 10% test.

The adversarial held-out set is NOT included in any of these splits —
it lives separately in data/adversarial_holdout_v1.jsonl and is used
purely for end-of-pipeline evaluation.
"""

import json
import random
from pathlib import Path
from collections import Counter, defaultdict

SEED = 42
SOURCE = Path("data/formatting_pairs_v1.jsonl")
OUT_DIR = Path("data/splits")


def main() -> None:
    rng = random.Random(SEED)

    # Load main dataset
    with SOURCE.open() as f:
        rows = [json.loads(line) for line in f]

    print(f"Loaded {len(rows)} examples from {SOURCE}\n")

    # Group by context for stratification
    by_context = defaultdict(list)
    for row in rows:
        by_context[row["context"]].append(row)

    # Split each context separately, then combine
    train, val, test = [], [], []
    for context, items in sorted(by_context.items()):
        shuffled = items[:]
        rng.shuffle(shuffled)
        n = len(shuffled)

        # 10% val + 10% test (with at least 1 in each)
        n_test = max(1, n // 10)
        n_val = max(1, n // 10)
        n_train = n - n_test - n_val

        train.extend(shuffled[:n_train])
        val.extend(shuffled[n_train:n_train + n_val])
        test.extend(shuffled[n_train + n_val:])

    # Re-shuffle each split so contexts are interleaved (not blocked)
    rng.shuffle(train)
    rng.shuffle(val)
    rng.shuffle(test)

    # Write splits
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, split in [("train", train), ("val", val), ("test", test)]:
        path = OUT_DIR / f"{name}.jsonl"
        with path.open("w") as f:
            for row in split:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(f"Wrote {len(split):4} examples to {path}")

    # Sanity check: no overlap between splits (by prompt)
    train_prompts = {r["prompt"] for r in train}
    val_prompts = {r["prompt"] for r in val}
    test_prompts = {r["prompt"] for r in test}

    assert not (train_prompts & val_prompts), "Train/val overlap detected"
    assert not (train_prompts & test_prompts), "Train/test overlap detected"
    assert not (val_prompts & test_prompts), "Val/test overlap detected"
    assert len(train) + len(val) + len(test) == len(rows), "Row count mismatch"

    print(f"\n  ✓ No overlap between splits")
    print(f"  ✓ Row counts sum to original ({len(rows)})")

    # Composition table
    train_c = Counter(r["context"] for r in train)
    val_c = Counter(r["context"] for r in val)
    test_c = Counter(r["context"] for r in test)
    all_contexts = sorted(set(train_c) | set(val_c) | set(test_c))

    print(f"\n=== STRATIFIED COMPOSITION (by context) ===\n")
    print(f"  {'context':<20} {'train':>6} {'val':>5} {'test':>5} {'total':>6}")
    print(f"  {'-' * 20}   {'-' * 6} {'-' * 5} {'-' * 5} {'-' * 6}")
    for ctx in all_contexts:
        t = train_c.get(ctx, 0)
        v = val_c.get(ctx, 0)
        te = test_c.get(ctx, 0)
        print(f"  {ctx:<20} {t:>6} {v:>5} {te:>5} {t + v + te:>6}")
    print(f"  {'-' * 20}   {'-' * 6} {'-' * 5} {'-' * 5} {'-' * 6}")
    print(f"  {'TOTAL':<20} {len(train):>6} {len(val):>5} {len(test):>5} {len(rows):>6}")

    pct_train = 100 * len(train) / len(rows)
    pct_val = 100 * len(val) / len(rows)
    pct_test = 100 * len(test) / len(rows)
    print(f"\n  Ratios: train {pct_train:.1f}% / val {pct_val:.1f}% / test {pct_test:.1f}%")
    print(f"  Seed: {SEED} (deterministic — re-running produces identical splits)")


if __name__ == "__main__":
    main()

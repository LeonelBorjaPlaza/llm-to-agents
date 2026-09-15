#!/usr/bin/env python3
"""
Recompute the negative-log-likelihood example in learn/training.qmd and
check every committed number: each per-position -log p, the sums and
means for both models, and the sequence-probability products quoted in
the prose.

The table is marked with <!-- check:likelihood --> and has the columns
  position | target | p_A | -log p_A | p_B | -log p_B
followed by "Sum" and "Mean" rows.

Usage: python3 scripts/check_training_example.py
Exit code 0 if every committed number matches within tolerance; 1 otherwise.
"""
import math
import re
import sys

LESSON_FILE = "learn/training.qmd"
TOLERANCE = 0.0015

ROW = re.compile(r"^\|\s*(\d)\s*\|\s*`[^`]*`\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|", re.M)
SUMMARY = re.compile(r"^\|\s*(Sum|Mean)\s*\|\s*\|\s*\|\s*([\d.]+)\s*\|\s*\|\s*([\d.]+)\s*\|", re.M)


def main():
    try:
        with open(LESSON_FILE, "r", encoding="utf-8") as fh:
            text = fh.read()
    except FileNotFoundError:
        print(f"FAIL: could not find {LESSON_FILE}")
        return 1

    start = text.find("<!-- check:likelihood -->")
    if start < 0:
        print(f"FAIL: could not find the likelihood table marker in {LESSON_FILE}")
        return 1
    block = text[start:]
    block = block[: block.find("\n## ")] if "\n## " in block else block

    rows = ROW.findall(block)
    summary = {name: (float(a), float(b)) for name, a, b in SUMMARY.findall(block)}
    if len(rows) < 2 or "Sum" not in summary or "Mean" not in summary:
        print(f"FAIL: could not parse the likelihood table (rows={len(rows)}, summary={sorted(summary)})")
        return 1

    ok = True

    def check(label, committed, expected):
        nonlocal ok
        if abs(committed - expected) > TOLERANCE:
            ok = False
            print(f"FAIL: {label}: lesson says {committed}, recomputed {expected:.4f}")

    p_a, p_b = [], []
    for pos, pa, la, pb, lb in rows:
        pa, pb = float(pa), float(pb)
        p_a.append(pa)
        p_b.append(pb)
        check(f"-log p_A at position {pos}", float(la), -math.log(pa))
        check(f"-log p_B at position {pos}", float(lb), -math.log(pb))
        if pb <= pa:
            ok = False
            print(f"FAIL: model B is supposed to assign more probability than model A at every position (position {pos})")

    sum_a = sum(-math.log(p) for p in p_a)
    sum_b = sum(-math.log(p) for p in p_b)
    check("Sum for model A", summary["Sum"][0], sum_a)
    check("Sum for model B", summary["Sum"][1], sum_b)
    check("Mean for model A", summary["Mean"][0], sum_a / len(p_a))
    check("Mean for model B", summary["Mean"][1], sum_b / len(p_b))

    # Sequence-probability products quoted in the prose.
    prod_a = math.prod(p_a)
    prod_b = math.prod(p_b)
    m = re.search(r"= ?\n?([\d.]+)\$, and \$-\\log [\d.]+ = ([\d.]+)\$", block)
    if m:
        committed_prod_a, committed_neglog_a = float(m.group(1)), float(m.group(2))
        if abs(committed_prod_a - prod_a) > 1e-5:
            ok = False
            print(f"FAIL: model A sequence probability: lesson says {committed_prod_a}, recomputed {prod_a:.5f}")
        check("-log of model A sequence probability", committed_neglog_a, -math.log(prod_a))
    else:
        ok = False
        print("FAIL: could not find model A's sequence-probability sentence in the prose")
    m = re.search(r"product is \$([\d.]+)\$ and its negative log is \$([\d.]+)\$", block)
    if m:
        if abs(float(m.group(1)) - prod_b) > 1e-5:
            ok = False
            print(f"FAIL: model B sequence probability: lesson says {m.group(1)}, recomputed {prod_b:.5f}")
        check("-log of model B sequence probability", float(m.group(2)), -math.log(prod_b))
    else:
        ok = False
        print("FAIL: could not find model B's sequence-probability sentence in the prose")

    if ok:
        print(f"PASS: likelihood example ({len(rows)} targets, two models) matches {LESSON_FILE}: "
              f"per-position losses, sums, means, and sequence probabilities all recompute.")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())

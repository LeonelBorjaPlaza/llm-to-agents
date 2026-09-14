#!/usr/bin/env python3
"""
Recompute the softmax-and-sampling interactive's static (no-JavaScript)
fallback table and bar chart from first principles, and check that the
numbers committed in _includes/_softmax-fallback.qmd still match.

This exists because the fallback content is hand-typed markdown -- if
whoever edits it next fat-fingers a digit, this is what catches it. It is
also the "small useful verification script" specified for this table by
the approved implementation plan.

Usage: python3 scripts/check_softmax_reference.py
Exit code 0 if every committed number matches the recomputation within
tolerance; 1 otherwise.
"""
import math
import re
import sys

TOKENS = ["repair", "monitor", "replace", "close", "ignore"]
LOGITS = [2.0, 1.0, 0.5, -0.5, -3.0]  # must match assets/js/softmax-lab.js DEFAULT_LOGITS
TEMPERATURES = [0.5, 1.0, 1.5]
FALLBACK_FILE = "_includes/_softmax-fallback.qmd"
TOLERANCE = 0.0005
BAR_SCALE = 300  # pixel width used for p=1.0 in the fallback SVG
BAR_TOLERANCE = 0.15  # pixels; committed widths are rounded to 1 decimal


def softmax(logits, temperature):
    scaled = [z / temperature for z in logits]
    m = max(scaled)
    exps = [math.exp(s - m) for s in scaled]
    total = sum(exps)
    return [e / total for e in exps]


def parse_committed_table(text):
    """Extract the |token|p@0.5|p@1.0|p@1.5| rows from the fallback file."""
    table = {}
    pattern = re.compile(
        r"^\|\s*(" + "|".join(TOKENS) + r")\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|",
        re.MULTILINE,
    )
    for match in pattern.finditer(text):
        token, p05, p10, p15 = match.groups()
        table[token] = [float(p05), float(p10), float(p15)]
    return table


def parse_committed_bar_widths(text):
    """Extract the SVG <rect width="..."> values, in token order, for T=1.0."""
    widths = {}
    for token in TOKENS:
        pattern = re.compile(
            r"<text[^>]*>" + re.escape(token) + r"\s*\(([\d.]+)\)</text>\s*"
            r"<rect[^>]*width=\"([\d.]+)\"",
        )
        match = pattern.search(text)
        if match:
            widths[token] = (float(match.group(1)), float(match.group(2)))
    return widths


def main():
    try:
        with open(FALLBACK_FILE, "r", encoding="utf-8") as fh:
            text = fh.read()
    except FileNotFoundError:
        print(f"FAIL: could not find {FALLBACK_FILE}")
        return 1

    computed = {
        token: [softmax(LOGITS, t)[i] for t in TEMPERATURES]
        for i, token in enumerate(TOKENS)
    }

    committed_table = parse_committed_table(text)
    committed_bars = parse_committed_bar_widths(text)

    ok = True

    if len(committed_table) != len(TOKENS):
        ok = False
        missing = set(TOKENS) - set(committed_table.keys())
        print(f"FAIL: fallback table is missing row(s) for: {sorted(missing)}")

    for token in TOKENS:
        if token not in committed_table:
            continue
        for i, temp in enumerate(TEMPERATURES):
            expected = computed[token][i]
            actual = committed_table[token][i]
            if abs(expected - actual) > TOLERANCE:
                ok = False
                print(
                    f"FAIL: {token} at T={temp}: fallback table says {actual:.4f}, "
                    f"recomputed {expected:.4f} (diff {abs(expected-actual):.4f} > tolerance {TOLERANCE})"
                )

    if len(committed_bars) != len(TOKENS):
        ok = False
        missing = set(TOKENS) - set(committed_bars.keys())
        print(f"FAIL: SVG bar chart is missing rect/label pair(s) for: {sorted(missing)}")

    for token in TOKENS:
        if token not in committed_bars:
            continue
        label_p, bar_width = committed_bars[token]
        expected_p = computed[token][1]  # T=1.0
        expected_width = expected_p * BAR_SCALE
        if abs(label_p - expected_p) > TOLERANCE:
            ok = False
            print(f"FAIL: {token} bar-chart label says p={label_p:.4f}, recomputed {expected_p:.4f}")
        if abs(bar_width - expected_width) > BAR_TOLERANCE:
            ok = False
            print(
                f"FAIL: {token} bar-chart rect width={bar_width}, expected ~{expected_width:.1f} "
                f"(p={expected_p:.4f} x {BAR_SCALE}px)"
            )

    if ok:
        print(f"PASS: all {len(TOKENS)} tokens x {len(TEMPERATURES)} temperatures match the fallback table")
        print("      and the T=1.0 bar chart matches the recomputed probabilities.")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())

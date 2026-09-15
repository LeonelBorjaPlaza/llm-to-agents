#!/usr/bin/env python3
"""
Recompute the one-head causal self-attention example in
learn/transformers-attention.qmd from the committed q/k/v vectors, and
check every committed score, attention weight, and output vector.

The lesson marks its four tables with HTML comments so this script can
find them without depending on prose:
  <!-- check:qkv -->      position | token | q | k | v
  <!-- check:scores -->   destination | s_i1 | s_i2 | s_i3   ("—" = masked)
  <!-- check:weights -->  destination | a_i1 | a_i2 | a_i3   ("—" = masked)
  <!-- check:outputs -->  destination | (y1, y2)

Usage: python3 scripts/check_attention_example.py
Exit code 0 if every committed number matches within tolerance; 1 otherwise.
"""
import math
import re
import sys

LESSON_FILE = "learn/transformers-attention.qmd"
TOLERANCE = 0.0015  # committed values are rounded to 3 decimals
D_K = 2

VEC = r"\(\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*\)"
QKV_ROW = re.compile(r"^\|\s*(\d)\s*\|\s*`[^`]*`\s*\|\s*" + VEC + r"\s*\|\s*" + VEC + r"\s*\|\s*" + VEC + r"\s*\|", re.M)
TRI_ROW = re.compile(r"^\|\s*(\d)\s*\|\s*([\d.]+|—)\s*\|\s*([\d.]+|—)\s*\|\s*([\d.]+|—)\s*\|", re.M)
OUT_ROW = re.compile(r"^\|\s*(\d)\s*\|\s*" + VEC + r"\s*\|", re.M)


def section(text, marker):
    """Return the text between a check marker and the next marker/heading."""
    start = text.find(f"<!-- check:{marker} -->")
    if start < 0:
        return ""
    rest = text[start + 1:]
    end = min([i for i in (rest.find("<!-- check:"), rest.find("\n## ")) if i >= 0] or [len(rest)])
    return rest[:end]


def parse_tri(block):
    rows = {}
    for i, *cells in TRI_ROW.findall(block):
        rows[int(i)] = [None if c == "—" else float(c) for c in cells]
    return rows


def main():
    try:
        with open(LESSON_FILE, "r", encoding="utf-8") as fh:
            text = fh.read()
    except FileNotFoundError:
        print(f"FAIL: could not find {LESSON_FILE}")
        return 1

    q, k, v = {}, {}, {}
    for row in QKV_ROW.findall(section(text, "qkv")):
        i = int(row[0])
        nums = [float(x) for x in row[1:]]
        q[i], k[i], v[i] = tuple(nums[0:2]), tuple(nums[2:4]), tuple(nums[4:6])
    scores = parse_tri(section(text, "scores"))
    weights = parse_tri(section(text, "weights"))
    outputs = {int(i): (float(a), float(b)) for i, a, b in OUT_ROW.findall(section(text, "outputs"))}

    n = len(q)
    if n < 2 or set(scores) != set(q) or set(weights) != set(q) or set(outputs) != set(q):
        print(f"FAIL: could not parse the four example tables from {LESSON_FILE} "
              f"(qkv={len(q)}, scores={len(scores)}, weights={len(weights)}, outputs={len(outputs)})")
        return 1

    ok = True

    def check(label, committed, expected):
        nonlocal ok
        if committed is None or abs(committed - expected) > TOLERANCE:
            ok = False
            print(f"FAIL: {label}: lesson says {committed}, recomputed {expected:.4f}")

    for i in sorted(q):
        permitted = [j for j in sorted(k) if j <= i]
        s = {j: (q[i][0] * k[j][0] + q[i][1] * k[j][1]) / math.sqrt(D_K) for j in permitted}
        m = max(s.values())
        e = {j: math.exp(s[j] - m) for j in permitted}
        z = sum(e.values())
        a = {j: e[j] / z for j in permitted}
        y = (sum(a[j] * v[j][0] for j in permitted), sum(a[j] * v[j][1] for j in permitted))

        for j in sorted(k):
            committed_s = scores[i][j - 1]
            committed_a = weights[i][j - 1]
            if j > i:
                # Masked: the lesson must show "—", never a number.
                if committed_s is not None or committed_a is not None:
                    ok = False
                    print(f"FAIL: entry ({i},{j}) should be masked but the lesson shows a number")
                continue
            check(f"s_{i}{j}", committed_s, s[j])
            check(f"a_{i}{j}", committed_a, a[j])
        if abs(sum(a.values()) - 1.0) > 1e-9:
            ok = False
            print(f"FAIL: recomputed weights for destination {i} do not sum to 1")
        check(f"y_{i}[1]", outputs[i][0], y[0])
        check(f"y_{i}[2]", outputs[i][1], y[1])

    if ok:
        print(f"PASS: {n}-position causal attention example (d_k={D_K}) matches {LESSON_FILE}: "
              f"scores, weights, masked entries, and outputs all recompute.")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())

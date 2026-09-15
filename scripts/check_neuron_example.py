#!/usr/bin/env python3
"""
Recompute the worked neuron/backprop/optimizer example in
learn/neural-networks.qmd from first principles, and check that every
number committed in that file still matches.

Same purpose and pattern as check_softmax_reference.py: catches a
hand-typed digit drifting from the actual arithmetic, without needing a
computational engine at Quarto render time.

Usage: python3 scripts/check_neuron_example.py
Exit code 0 if every committed number matches the recomputation within
tolerance; 1 otherwise.
"""
import math
import re
import sys

LESSON_FILE = "learn/neural-networks.qmd"
TOLERANCE = 0.0005

# Inputs and parameters, matching the .qmd's stated toy example exactly.
X1, X2 = 1.0, 2.0
W1, W2, B = 0.5, -1.0, 0.3
Y_TARGET = 1.0
ETA = 0.1


def sigmoid(a):
    return 1.0 / (1.0 + math.exp(-a))


def compute():
    values = {}

    a = W1 * X1 + W2 * X2 + B
    values["a"] = a

    yhat = sigmoid(a)
    values["yhat"] = yhat

    loss = -math.log(yhat)  # cross-entropy with y_target = 1
    values["loss"] = loss

    dL_da = yhat - Y_TARGET
    values["dL_da"] = dL_da

    dL_dw1 = dL_da * X1
    dL_dw2 = dL_da * X2
    dL_db = dL_da * 1.0
    values["dL_dw1"] = dL_dw1
    values["dL_dw2"] = dL_dw2
    values["dL_db"] = dL_db

    w1_new = W1 - ETA * dL_dw1
    w2_new = W2 - ETA * dL_dw2
    b_new = B - ETA * dL_db
    values["w1_new"] = w1_new
    values["w2_new"] = w2_new
    values["b_new"] = b_new

    a_new = w1_new * X1 + w2_new * X2 + b_new
    values["a_new"] = a_new

    yhat_new = sigmoid(a_new)
    values["yhat_new"] = yhat_new

    loss_new = -math.log(yhat_new)
    values["loss_new"] = loss_new

    return values


# Each pattern's single capture group is the committed value in the .qmd,
# keyed by a substring unique enough in the file to anchor on reliably.
PATTERNS = {
    "a": r"0\.5 - 2\.0 \+ 0\.3 = (-?[\d.]+)",
    "yhat": r"e\^\{1\.2\}\}\s*\\approx\s*(-?[\d.]+)",
    "loss": r"L = -\\log\(0\.231475\) \\approx (-?[\d.]+)",
    "dL_da": r"0\.231475 - 1 = (-?[\d.]+)",
    "dL_dw1": r"\\cdot x_1\s*\n= \(-?[\d.]+\)\(1\.0\) = (-?[\d.]+)",
    "dL_dw2": r"\\cdot x_2\s*\n= \(-?[\d.]+\)\(2\.0\) = (-?[\d.]+)",
    "dL_db": r"\\cdot 1\s*\n= (-?[\d.]+)",
    "w1_new": r"w_1 \\to 0\.5 - 0\.1\(-?[\d.]+\) = (-?[\d.]+)",
    "w2_new": r"w_2 \\to -1\.0 - 0\.1\(-?[\d.]+\) = (-?[\d.]+)",
    "b_new": r"b \\to 0\.3 - 0\.1\(-?[\d.]+\) = (-?[\d.]+)",
    "a_new": r"a_\{\\text\{new\}\}.*\\approx\s*(-?[\d.]+)",
    "yhat_new": r"\\sigma\(-0\.738885\) \\approx (-?[\d.]+)",
    "loss_new": r"L_\{\\text\{new\}\} = -\\log\(0\.323248\) \\approx (-?[\d.]+)",
}


def parse_committed(text):
    committed = {}
    missing = []
    for name, pattern in PATTERNS.items():
        match = re.search(pattern, text)
        if match:
            committed[name] = float(match.group(1))
        else:
            missing.append(name)
    return committed, missing


def main():
    try:
        with open(LESSON_FILE, "r", encoding="utf-8") as fh:
            text = fh.read()
    except FileNotFoundError:
        print(f"FAIL: could not find {LESSON_FILE}")
        return 1

    computed = compute()
    committed, missing = parse_committed(text)

    ok = True

    if missing:
        ok = False
        print(f"FAIL: could not find {len(missing)} committed value(s) in {LESSON_FILE}: {missing}")

    for name, expected in computed.items():
        if name not in committed:
            continue
        actual = committed[name]
        if abs(expected - actual) > TOLERANCE:
            ok = False
            print(
                f"FAIL: {name}: {LESSON_FILE} says {actual}, recomputed {expected:.6f} "
                f"(diff {abs(expected-actual):.6f} > tolerance {TOLERANCE})"
            )

    if ok:
        print(f"PASS: all {len(computed)} recomputed values match {LESSON_FILE}'s worked example.")
        print(f"      a={computed['a']:.4f}  yhat={computed['yhat']:.6f}  loss={computed['loss']:.4f}")
        print(f"      loss_new={computed['loss_new']:.4f} (< loss, confirming the step improved the fit)")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())

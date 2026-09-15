#!/usr/bin/env python3
"""
Recompute the recurrent-vs-self-attention path-length and sequential-
operations figures used in learn/why-transformers.qmd, for the toy n=8
example and for a few other sequence lengths, and check the n=8 numbers
against what is actually written in that lesson.

These are simple, exact instantiations of the asymptotic (big-O) bounds
Vaswani et al.'s Table 1 states -- not the paper's own literal numbers,
which are asymptotic, not per-n. See sources/claims.csv (S-16, S-17) for
the distinction between "the paper says O(n)/O(1)" and "this course's own
n=8 arithmetic instantiation of that bound."

The lesson commits three recurrent figures for n=8, and this script checks
each one separately, because they are different quantities:
  - the path from position 2 to position 8 (the toy anaphora example):
    j - i = 6 sequential steps;
  - the longest path in the sequence, position 1 to position 8:
    n - 1 = 7 sequential steps;
  - processing the whole sequence once: n = 8 sequential steps.
An earlier version of the lesson attached the 1-to-8 figure (7) to the
2-to-8 example; this script now distinguishes the two endpoints so that
conflation cannot pass silently.

Usage: python3 scripts/check_transformer_path_lengths.py
Exit code 0 if the n=8 figures committed in the lesson match the
recomputation, and the general growth pattern holds across every tested
n; 1 otherwise.
"""
import re
import sys

LESSON_FILE = "learn/why-transformers.qmd"
TOY_N = 8
TOY_FROM, TOY_TO = 2, 8  # the anaphora example: "it" at 8 refers back to 2
TEST_NS = [4, 8, 16, 64]


def path_length_rnn(i, j):
    """Sequential steps needed to carry information from position i to a
    later position j in a naive left-to-right recurrent chain: one step
    per transition i->i+1, ..., j-1->j."""
    assert 1 <= i <= j
    return j - i


def max_path_length_rnn(n):
    """Longest path in a recurrent chain of length n: position 1 to
    position n."""
    return path_length_rnn(1, n)


def seq_ops_rnn(n):
    """Minimum sequential steps to process the sequence once, recurrently."""
    return n


def path_length_attn(_i, _j):
    """Path length between any two permitted positions in one
    self-attention layer: constant (O(1)), per Vaswani et al. Table 1."""
    return 1


def seq_ops_attn(_n):
    """Minimum sequential operations for one self-attention layer, given
    the full input: constant in n (O(1)), per Vaswani et al. Table 1."""
    return 1


def check_committed(text, label, pattern, expected):
    match = re.search(pattern, text)
    if not match:
        print(f"FAIL: could not find the committed '{label}' figure in {LESSON_FILE}")
        return False
    committed = int(match.group(1))
    if committed != expected:
        print(f"FAIL: lesson states {committed} for '{label}'; recomputed {expected}")
        return False
    return True


def main():
    try:
        with open(LESSON_FILE, "r", encoding="utf-8") as fh:
            text = fh.read()
    except FileNotFoundError:
        print(f"FAIL: could not find {LESSON_FILE}")
        return 1

    ok = True

    # --- 1. Check the three committed n=8 recurrent figures, separately.
    ok &= check_committed(
        text,
        f"position {TOY_FROM} to position {TOY_TO}",
        rf"position {TOY_FROM} to position {TOY_TO} takes\s+\*\*(\d+) sequential steps\*\*",
        path_length_rnn(TOY_FROM, TOY_TO),
    )
    ok &= check_committed(
        text,
        f"longest path, position 1 to position {TOY_N}",
        rf"from position 1 to position {TOY_N}, takes\s+\*\*(\d+) sequential steps\*\*",
        max_path_length_rnn(TOY_N),
    )
    ok &= check_committed(
        text,
        "total sequential steps to process the sequence",
        r"requires\s+\*\*(\d+) sequential steps\*\* in total",
        seq_ops_rnn(TOY_N),
    )

    # --- 2. Check the qualitative one-step attention claim is actually present.
    one_step_claim = re.search(
        rf"position {TOY_TO} can attend directly to\s+position {TOY_FROM}, in one step", text
    )
    if not one_step_claim:
        ok = False
        print(f"FAIL: could not find the expected one-step self-attention claim for the n={TOY_N} example in {LESSON_FILE}")

    # --- 3. Demonstrate and assert the general growth pattern across several n.
    print(f"{'n':>4} | {'maxpath_rnn':>11} {'ops_rnn':>8} | {'path_attn':>10} {'ops_attn':>9}")
    for n in TEST_NS:
        p_rnn, o_rnn = max_path_length_rnn(n), seq_ops_rnn(n)
        p_attn, o_attn = path_length_attn(1, n), seq_ops_attn(n)
        print(f"{n:>4} | {p_rnn:>11} {o_rnn:>8} | {p_attn:>10} {o_attn:>9}")
        if p_rnn != n - 1 or o_rnn != n:
            ok = False
            print(f"FAIL: recurrent figures at n={n} do not match the O(n) formula")
        if p_attn != 1 or o_attn != 1:
            ok = False
            print(f"FAIL: attention figures at n={n} are not constant at 1 (O(1))")

    if not (max_path_length_rnn(TEST_NS[-1]) > max_path_length_rnn(TEST_NS[0])):
        ok = False
        print("FAIL: recurrent path length does not grow with n as expected")
    if not (path_length_attn(1, TEST_NS[-1]) == path_length_attn(1, TEST_NS[0])):
        ok = False
        print("FAIL: attention path length is not constant across n as expected")

    if ok:
        print(
            f"PASS: n={TOY_N} figures match the lesson "
            f"({TOY_FROM}->{TOY_TO}: {path_length_rnn(TOY_FROM, TOY_TO)}, "
            f"1->{TOY_N}: {max_path_length_rnn(TOY_N)}, total: {seq_ops_rnn(TOY_N)}); "
            f"O(n) vs O(1) growth pattern confirmed across n={TEST_NS}."
        )
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())

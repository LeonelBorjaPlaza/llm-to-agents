#!/usr/bin/env python3
"""
Recompute the two small numerical examples in learn/tokens-context.qmd and
check them against what is written there:

  1. the BPE-style merge example (Section 3): from the committed word
     counts, re-run the merge procedure (merge the most frequent adjacent
     pair, weighted by word count) and check each committed merge step's
     pair, count, and new vocabulary entry, plus the committed final split
     of every word;
  2. the context-budget arithmetic (Section 9): the committed "Remaining"
     figure must equal the window minus the listed items.

Same purpose and pattern as check_neuron_example.py: catch a hand-typed
number drifting from the arithmetic, with no computational engine at
Quarto render time.

Usage: python3 scripts/check_bpe_example.py
Exit code 0 if everything matches; 1 otherwise.
"""
import re
import sys
from collections import Counter

LESSON_FILE = "learn/tokens-context.qmd"

WORD_ROW = re.compile(r"^\|\s*`([a-z]+)`\s*\|\s*(\d+)\s*\|\s*$", re.MULTILINE)
MERGE_ROW = re.compile(
    r"^\|\s*(\d+)\s*\|\s*`([a-z]+)`\s*\+\s*`([a-z]+)`\s*\|\s*(\d+)\s*\|\s*`([a-z]+)`\s*\|\s*$",
    re.MULTILINE,
)
SPLIT_ROW = re.compile(r"^- `([a-z]+)` → ((?:`[a-z]+`\s*)+)$", re.MULTILINE)
# Budget rows have a plain-text label; the BPE word table's labels are in
# backticks, so require the label to start with a letter.
BUDGET_ROW = re.compile(r"^\|\s*([A-Za-z][^|]*?)\s*\|\s*([\d,]+)\s*\|\s*$", re.MULTILINE)


def bpe_merges(words, n_merges):
    """Run n_merges BPE merges over `words` (word -> count). Returns the
    list of (pair, count, new_symbol) steps and the final segmentation."""
    seqs = {w: list(w) for w in words}
    steps = []
    for _ in range(n_merges):
        pairs = Counter()
        for w, s in seqs.items():
            for a, b in zip(s, s[1:]):
                pairs[(a, b)] += words[w]
        (a, b), count = pairs.most_common(1)[0]
        # Refuse ties silently passing: the lesson's example must be unambiguous.
        ranked = pairs.most_common(2)
        if len(ranked) == 2 and ranked[1][1] == count:
            raise ValueError(f"tie at count {count} between {ranked[0][0]} and {ranked[1][0]}")
        for w, s in seqs.items():
            out, i = [], 0
            while i < len(s):
                if i + 1 < len(s) and s[i] == a and s[i + 1] == b:
                    out.append(a + b)
                    i += 2
                else:
                    out.append(s[i])
                    i += 1
            seqs[w] = out
        steps.append(((a, b), count, a + b))
    return steps, seqs


def main():
    try:
        with open(LESSON_FILE, "r", encoding="utf-8") as fh:
            text = fh.read()
    except FileNotFoundError:
        print(f"FAIL: could not find {LESSON_FILE}")
        return 1

    ok = True

    # --- 1. BPE example.
    words = {w: int(c) for w, c in WORD_ROW.findall(text)}
    merges = MERGE_ROW.findall(text)
    splits = {w: re.findall(r"`([a-z]+)`", parts) for w, parts in SPLIT_ROW.findall(text)}

    if len(words) < 2 or not merges or not splits:
        print(f"FAIL: could not parse the BPE example tables from {LESSON_FILE} "
              f"(words={len(words)}, merges={len(merges)}, splits={len(splits)})")
        return 1

    try:
        steps, final = bpe_merges(words, len(merges))
    except ValueError as exc:
        print(f"FAIL: BPE example is ambiguous: {exc}")
        return 1

    for (step_no, a, b, count, new), ((ea, eb), ecount, enew) in zip(merges, steps):
        if (a, b) != (ea, eb) or int(count) != ecount or new != enew:
            ok = False
            print(f"FAIL: merge {step_no}: lesson says `{a}`+`{b}` ({count}) -> `{new}`; "
                  f"recomputed `{ea}`+`{eb}` ({ecount}) -> `{enew}`")

    for w, committed in splits.items():
        if w not in final:
            ok = False
            print(f"FAIL: final split listed for `{w}`, which is not in the word table")
        elif committed != final[w]:
            ok = False
            print(f"FAIL: final split of `{w}`: lesson says {committed}, recomputed {final[w]}")
    for w in final:
        if w not in splits:
            ok = False
            print(f"FAIL: no final split listed for `{w}`")

    # --- 2. Context-budget arithmetic.
    budget = {label.strip(): int(num.replace(",", "")) for label, num in BUDGET_ROW.findall(text)}
    window_key = next((k for k in budget if k.lower().startswith("window")), None)
    if window_key is None or "Remaining" not in budget:
        ok = False
        print(f"FAIL: could not parse the context-budget table from {LESSON_FILE}")
    else:
        used = sum(v for k, v in budget.items() if k not in (window_key, "Remaining"))
        expected_remaining = budget[window_key] - used
        if expected_remaining != budget["Remaining"]:
            ok = False
            print(f"FAIL: budget table says Remaining = {budget['Remaining']:,}; "
                  f"recomputed {budget[window_key]:,} - {used:,} = {expected_remaining:,}")
        used_in_prose = re.search(r"The ([\d,]+) tokens already used", text)
        if used_in_prose and int(used_in_prose.group(1).replace(",", "")) != used:
            ok = False
            print(f"FAIL: prose says {used_in_prose.group(1)} tokens already used; recomputed {used:,}")

    if ok:
        print(f"PASS: BPE example ({len(words)} words, {len(merges)} merges) and context-budget "
              f"arithmetic match {LESSON_FILE}.")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())

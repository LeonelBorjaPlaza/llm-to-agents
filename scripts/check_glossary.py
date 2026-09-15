#!/usr/bin/env python3
"""
Check glossary.qmd for the failure modes a glossary actually has:

  * duplicate entry headings or duplicate anchor ids;
  * a required core term missing;
  * an entry with no "Taught in" pointer and no "See" cross-reference;
  * a cross-reference (#anchor) that names no entry on the page;
  * a "Taught in" link whose target .qmd file does not exist;
  * entries out of alphabetical order within a letter section, or a
    letter section whose entries do not start with that letter.

Rendered-link resolution (that #anchors exist in the built HTML) is
already covered by scripts/check_links.py; this script checks the source
so that a mistake is caught before render and reported by entry name.

Usage: python3 scripts/check_glossary.py [glossary.qmd]
Exit code 0 if every check passes; 1 otherwise.
"""
import os
import re
import sys

REQUIRED_IDS = [
    "token", "tokenizer", "vocabulary", "token-id", "embedding",
    "contextual-representation", "parameter", "weight", "bias",
    "activation-function", "layer", "neural-network", "forward-pass",
    "loss", "gradient", "gradient-descent", "backpropagation", "optimizer",
    "transformer", "transformer-block", "self-attention", "query", "key",
    "value", "attention-head", "attention-weight", "causal-mask",
    "feed-forward-layer", "residual-connection", "normalization", "logit",
    "softmax", "temperature", "sampling", "argmax", "context-window",
    "context", "prompt", "system-prompt", "pretraining",
    "autoregressive-model", "negative-log-likelihood", "cross-entropy",
    "maximum-likelihood", "post-training", "supervised-fine-tuning",
    "preference-data", "reward-model", "reinforcement-learning", "rlhf",
    "direct-preference-optimization", "reasoning-tokens", "inference",
    "retrieval", "tool", "tool-call", "assistant", "workflow", "agent",
    "state", "external-state", "memory", "skill", "verification",
    "prompt-caching", "context-engineering",
]

LETTER_RE = re.compile(r"^## ([A-Z]) \{#([a-z])\}\s*$")
ENTRY_RE = re.compile(r"^### (.+?) \{#([a-z0-9-]+)\}\s*$")
ANCHOR_RE = re.compile(r"\]\(#([a-z0-9-]+)\)")
FILE_LINK_RE = re.compile(r"\]\(((?:learn/)?[a-z-]+\.qmd)\)")


def sort_key(title: str) -> str:
    # Word-by-word dictionary order: keep spaces (which sort before
    # letters), drop other punctuation, so "context window" precedes
    # "contextual representation".
    return re.sub(r"[^a-z0-9 ]", "", title.lower()).strip()


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "glossary.qmd"
    with open(path, "r", encoding="utf-8") as fh:
        lines = fh.read().splitlines()

    failures = []
    entries = []  # (title, id, letter, body_lines)
    current_letter = None
    current = None
    for line in lines:
        m = LETTER_RE.match(line)
        if m:
            if m.group(1).lower() != m.group(2):
                failures.append(f"letter heading '{line}' has a mismatched id")
            current_letter = m.group(1)
            current = None
            continue
        m = ENTRY_RE.match(line)
        if m:
            current = [m.group(1), m.group(2), current_letter, []]
            entries.append(current)
            continue
        if line.startswith("### "):
            failures.append(f"entry heading without an explicit {{#id}}: '{line}'")
            current = None
            continue
        if current is not None:
            current[3].append(line)

    if not entries:
        print("FAIL: no glossary entries found.")
        return 1

    ids = [e[1] for e in entries]
    titles = [sort_key(e[0]) for e in entries]
    for dup in sorted({i for i in ids if ids.count(i) > 1}):
        failures.append(f"duplicate anchor id '#{dup}'")
    for dup in sorted({t for t in titles if titles.count(t) > 1}):
        failures.append(f"duplicate entry title (normalized) '{dup}'")

    id_set = set(ids)
    for req in REQUIRED_IDS:
        if req not in id_set:
            failures.append(f"required core term missing: '#{req}'")

    # Alphabetical order within each letter, and letter membership.
    by_letter = {}
    for title, eid, letter, _ in entries:
        if letter is None:
            failures.append(f"entry '{title}' appears before any letter heading")
            continue
        by_letter.setdefault(letter, []).append(title)
        if not sort_key(title).startswith(letter.lower()):
            failures.append(f"entry '{title}' is filed under '{letter}'")
    for letter, titles_in in by_letter.items():
        keys = [sort_key(t) for t in titles_in]
        if keys != sorted(keys):
            failures.append(f"entries under '{letter}' are not in alphabetical order: {titles_in}")
    letters = list(by_letter.keys())
    if letters != sorted(letters):
        failures.append(f"letter sections are not in order: {letters}")

    # Every entry points somewhere; every cross-reference and file link resolves.
    for title, eid, _, body in entries:
        text = "\n".join(body)
        has_taught = "*Taught in" in text
        has_see = re.search(r"\bSee \[", text) is not None
        if not (has_taught or has_see):
            failures.append(f"entry '{title}' has neither a 'Taught in' pointer nor a 'See' cross-reference")
        for anchor in ANCHOR_RE.findall(text):
            if anchor not in id_set:
                failures.append(f"entry '{title}' cross-references '#{anchor}', which is not an entry")
        for target in FILE_LINK_RE.findall(text):
            if not os.path.isfile(target):
                failures.append(f"entry '{title}' links to '{target}', which does not exist")

    if failures:
        print(f"FAIL: {len(failures)} glossary problem(s):")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(
        f"PASS: {len(entries)} glossary entries under {len(by_letter)} letters; "
        f"ids unique, {len(REQUIRED_IDS)} required terms present, order and links check out."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

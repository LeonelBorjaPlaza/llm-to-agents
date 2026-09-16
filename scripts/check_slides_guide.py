#!/usr/bin/env python3
"""
Reconcile the live deck with its speaking guide.

Every slide in slides/llms-to-agents.qmd (a level-two heading with an
explicit {#id}, plus the title slide Quarto generates from the front
matter) must have exactly one section in slides/speaking-guide.qmd whose
heading carries the same id and the same title text, and the guide must
not describe slides that do not exist. The guide's per-slide time
estimates must add up to the talk's stated target range.

Usage: python3 scripts/check_slides_guide.py
Exit code 0 if deck and guide reconcile; 1 otherwise.
"""
import re
import sys

DECK = "slides/llms-to-agents.qmd"
GUIDE = "slides/speaking-guide.qmd"
TARGET_MIN, TARGET_MAX = 35.0, 40.0

DECK_HEADING = re.compile(r"^## (.+?) \{#([a-z0-9-]+)(?:\s+[^}]*)?\}\s*$", re.M)
GUIDE_HEADING = re.compile(r"^## (.+?) \{#([a-z0-9-]+)\}\s*$", re.M)
GUIDE_TIME = re.compile(r"\*\*Time:\*\*\s*about\s+([0-9.]+)\s*min", re.I)


def main():
    deck = open(DECK, encoding="utf-8").read()
    guide = open(GUIDE, encoding="utf-8").read()
    failures = []

    deck_slides = [(sid, title) for title, sid in DECK_HEADING.findall(deck)]
    fm = deck.split("---")[1] if deck.startswith("---") else ""
    m = re.search(r'^title:\s*"?([^"\n]+)"?\s*$', fm, re.M)
    if m:
        deck_slides.insert(0, ("title-slide", m.group(1).strip()))

    guide_sections = [(sid, title) for title, sid in GUIDE_HEADING.findall(guide)]
    guide_map = {}
    for sid, title in guide_sections:
        if sid in guide_map:
            failures.append(f"guide has two sections with id '{sid}'")
        guide_map[sid] = title

    deck_ids = [sid for sid, _ in deck_slides]
    for dup in sorted({i for i in deck_ids if deck_ids.count(i) > 1}):
        failures.append(f"deck has duplicate slide id '{dup}'")

    for sid, title in deck_slides:
        if sid not in guide_map:
            failures.append(f"slide '{sid}' has no guide section")
        elif guide_map[sid] != title:
            failures.append(f"title mismatch for '{sid}': deck '{title}' vs guide '{guide_map[sid]}'")
    for sid in guide_map:
        if sid not in deck_ids and sid not in ("running-late",):
            failures.append(f"guide section '{sid}' does not correspond to a slide")

    guide_order = [sid for sid, _ in guide_sections if sid in deck_ids]
    if guide_order != [sid for sid in deck_ids if sid in guide_map]:
        failures.append("guide sections are not in slide order")

    times = [float(t) for t in GUIDE_TIME.findall(guide)]
    total = sum(times)
    if len(times) != len(deck_slides):
        failures.append(f"guide has {len(times)} time estimates for {len(deck_slides)} slides")
    if not (TARGET_MIN <= total <= TARGET_MAX):
        failures.append(f"guide time estimates sum to {total:.1f} min, outside {TARGET_MIN:.0f}-{TARGET_MAX:.0f}")

    if failures:
        print(f"FAIL: {len(failures)} deck/guide problem(s):")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(f"PASS: {len(deck_slides)} slides reconcile with the speaking guide; estimates sum to {total:.1f} min.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

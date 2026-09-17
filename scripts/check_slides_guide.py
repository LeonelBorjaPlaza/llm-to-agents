#!/usr/bin/env python3
"""
Reconcile the live deck with its speaking guide.

Deck slides are level-two headings with an explicit {#id} in
slides/llms-to-agents.qmd, plus the title slide Quarto generates from the
front matter. A slide carrying the class `.backup` is outside the prepared
route. The guide (slides/speaking-guide.qmd) must have exactly one section
per slide with the same id and title, in the same order for the prepared
route, with backup slides handled separately:

  * every prepared slide's guide section states "**Time:** about N min
    (running total M)"; the N values must add up to PREPARED_MINUTES and
    each running total must equal the sum so far;
  * every backup slide's guide section states "**Time:** backup";
  * the guide states the reserve (RESERVE_MINUTES) and the slot total.

Usage: python3 scripts/check_slides_guide.py
Exit code 0 if deck and guide reconcile; 1 otherwise.
"""
import re
import sys

DECK = "slides/llms-to-agents.qmd"
GUIDE = "slides/speaking-guide.qmd"
PREPARED_MINUTES = 28.0
RESERVE_MINUTES = 2.0
SLOT_MINUTES = 30.0

DECK_HEADING = re.compile(r"^## (.+?) \{#([a-z0-9-]+)((?:\s+\.[a-z0-9-]+)*)\}\s*$", re.M)
GUIDE_HEADING = re.compile(r"^## (.+?) \{#([a-z0-9-]+)\}\s*$", re.M)
TIME_LINE = re.compile(r"\*\*Time:\*\*\s*(?:about\s+([0-9.]+)\s*min\s*\(running\s+total\s+([0-9.]+)\)|(backup))", re.I)


def main():
    deck = open(DECK, encoding="utf-8").read()
    guide = open(GUIDE, encoding="utf-8").read()
    failures = []

    slides = []  # (id, title, is_backup)
    fm = deck.split("---")[1] if deck.startswith("---") else ""
    m = re.search(r'^title:\s*"?([^"\n]+)"?\s*$', fm, re.M)
    if m:
        slides.append(("title-slide", m.group(1).strip(), False))
    for title, sid, classes in DECK_HEADING.findall(deck):
        slides.append((sid, title, ".backup" in classes))
    ids = [s[0] for s in slides]
    for dup in sorted({i for i in ids if ids.count(i) > 1}):
        failures.append(f"deck has duplicate slide id '{dup}'")
    prepared = [s for s in slides if not s[2]]
    backup = [s for s in slides if s[2]]
    # Backup slides must come after every prepared slide.
    if backup:
        last_prepared = max(i for i, s in enumerate(slides) if not s[2])
        first_backup = min(i for i, s in enumerate(slides) if s[2])
        if first_backup < last_prepared:
            failures.append("a backup slide sits inside the prepared route")

    # Guide sections, in order, with their time lines.
    sections = []  # (id, title, minutes or None, running or None, is_backup)
    parts = GUIDE_HEADING.split(guide)
    # parts: [preamble, title1, id1, body1, title2, id2, body2, ...]
    for i in range(1, len(parts), 3):
        title, sid, body = parts[i], parts[i + 1], parts[i + 2]
        t = TIME_LINE.search(body)
        if t is None:
            sections.append((sid, title, None, None, None))
        elif t.group(3):
            sections.append((sid, title, None, None, True))
        else:
            sections.append((sid, title, float(t.group(1)), float(t.group(2)), False))
    guide_map = {}
    for sid, title, minutes, running, is_backup in sections:
        if sid in guide_map:
            failures.append(f"guide has two sections with id '{sid}'")
        guide_map[sid] = (title, minutes, running, is_backup)

    for sid, title, is_backup in slides:
        if sid not in guide_map:
            failures.append(f"slide '{sid}' has no guide section")
            continue
        gtitle, minutes, running, gbackup = guide_map[sid]
        if gtitle != title:
            failures.append(f"title mismatch for '{sid}': deck '{title}' vs guide '{gtitle}'")
        if gbackup is None:
            failures.append(f"guide section '{sid}' has no recognizable Time line")
        elif is_backup and not gbackup:
            failures.append(f"backup slide '{sid}' has a timed guide section; it should say 'Time: backup'")
        elif not is_backup and gbackup:
            failures.append(f"prepared slide '{sid}' is marked backup in the guide")
    for sid in guide_map:
        if sid not in ids and sid != "running-late":
            failures.append(f"guide section '{sid}' does not correspond to a slide")

    # Order and timing arithmetic over the prepared route.
    guide_order = [s[0] for s in sections if s[0] in ids and not s[4]]
    deck_order = [s[0] for s in prepared if s[0] in guide_map]
    if guide_order != deck_order:
        failures.append("guide sections are not in the deck's prepared order")
    total = 0.0
    for sid, _, _ in prepared:
        entry = guide_map.get(sid)
        if entry and entry[1] is not None:
            total += entry[1]
            if abs(total - entry[2]) > 0.011:
                failures.append(f"running total for '{sid}' is {entry[2]}, expected {total:.2f}")
    if abs(total - PREPARED_MINUTES) > 0.011:
        failures.append(f"prepared estimates sum to {total:.2f} min, expected {PREPARED_MINUTES:.1f}")
    if not re.search(r"\b2[\s-]*minutes?\b.*\breserve\b|\breserve\b.*\b2[\s-]*minutes?\b", guide, re.I | re.S):
        failures.append("guide does not state the 2-minute reserve")
    if not re.search(r"30-minute", guide):
        failures.append("guide does not state the 30-minute slot")

    if failures:
        print(f"FAIL: {len(failures)} deck/guide problem(s):")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(
        f"PASS: {len(prepared)} prepared slides and {len(backup)} backup slide(s) reconcile with the guide; "
        f"estimates sum to {total:.1f} min prepared + {RESERVE_MINUTES:.0f} min reserve = {SLOT_MINUTES:.0f} min."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

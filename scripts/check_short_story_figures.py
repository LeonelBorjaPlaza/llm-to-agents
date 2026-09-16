#!/usr/bin/env python3
"""
Check that every required Short Story figure is actually present in the
rendered page, and that no figure include exists without being used.

Two failure modes this guards against:
  * a figure that exists as an include but was never inserted into
    short-story.qmd (or whose include directive failed silently), so the
    rendered page lacks its wrapper id;
  * a figure include under _includes/ that no page includes at all.

Usage: python3 scripts/check_short_story_figures.py [site_dir]
Exit code 0 if every required id renders and every figure include is
used; 1 otherwise.
"""
import glob
import os
import re
import sys

REQUIRED_IDS = [
    "fig-lifecycle",
    "fig-runnable-model",
    "fig-tiny-network",
    "fig-data-pipeline",
    "fig-token-vector",
    "fig-rnn-transformer",
    "fig-attention-intuition",
    "fig-training-stages",
    "fig-reasoning-compute",
    "fig-inference-loop",
    "fig-three-stores",
    "fig-tool-roundtrip",
    "fig-agent-loop",
]


def main():
    site_dir = sys.argv[1] if len(sys.argv) > 1 else "_site"
    page = os.path.join(site_dir, "short-story.html")
    if not os.path.isfile(page):
        print(f"FAIL: '{page}' does not exist. Run `quarto render` first.")
        return 1
    html = open(page, "r", encoding="utf-8", errors="replace").read()
    failures = []

    # 1. Every required wrapper id renders, in narrative order.
    positions = []
    for fid in REQUIRED_IDS:
        m = re.search(r'<figure id="%s"' % re.escape(fid), html)
        if not m:
            failures.append(f"required figure '{fid}' is not in the rendered short story")
        else:
            positions.append((m.start(), fid))
    rendered_order = [fid for _, fid in sorted(positions)]
    expected_order = [fid for fid in REQUIRED_IDS if fid in rendered_order]
    if rendered_order != expected_order:
        failures.append(f"figures render out of narrative order: {rendered_order}")

    # 2. Every figure include is used by at least one source page.
    sources = ""
    for pattern in ("*.qmd", "learn/*.qmd", "slides/*.qmd", "_includes/*.qmd"):
        for path in glob.glob(pattern):
            sources += open(path, "r", encoding="utf-8", errors="replace").read()
    for inc in sorted(glob.glob("_includes/_fig-*.qmd")):
        name = os.path.basename(inc)
        if name not in sources:
            failures.append(f"figure include '{inc}' is not included by any page")

    if failures:
        print(f"FAIL: {len(failures)} figure problem(s):")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(
        f"PASS: all {len(REQUIRED_IDS)} required Short Story figures render in order; "
        f"every _includes/_fig-*.qmd is used."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

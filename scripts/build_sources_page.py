#!/usr/bin/env python3
"""
Generate sources.qmd, the public Sources page, from sources/claims.csv.

Every claim marker on the site ([S-nn] in the source files) is rendered as a
link to the matching entry on this page by filters/course-links.lua, so the
page must exist and must agree with the CSV. Run this script after editing
claims.csv; run it with --check (as scripts/verify.sh does) to confirm the
committed page is current.

Usage: python3 scripts/build_sources_page.py [--check]
Exit code 0 on success (or when --check finds the page current); 1 if
--check finds the page stale.
"""
import csv
import sys

CSV = "sources/claims.csv"
OUT = "sources.qmd"


def esc(text):
    # Escape Markdown so claim text renders literally (backslash escapes are
    # honored by Pandoc for these characters).
    for ch in "\\`*_{}[]<>#$":
        text = text.replace(ch, "\\" + ch)
    return text


def build():
    rows = list(csv.DictReader(open(CSV, encoding="utf-8", newline="")))
    lines = [
        "---",
        'title: "Sources"',
        'subtitle: "Every factual claim on this site, with the evidence behind it"',
        "toc: false",
        "---",
        "",
        "*Claims on this site carry a marker such as S-05 that links here. Each",
        "entry gives the claim as the course states it, the source, where in the",
        "source it is supported, whether the support is direct or a course",
        "inference, a confidence level, and any caveat. The machine-checked",
        "ledger is `sources/claims.csv` in the repository; `sources/source-map.md`",
        "describes each source in prose. This page is generated from the ledger.*",
        "",
        f"{len(rows)} claims.",
        "",
        "::: {.sources-list}",
        "",
    ]
    for r in rows:
        cid = r["id"].strip()
        anchor = cid.lower()
        lines += [
            f"### {cid} {{#{anchor}}}",
            "",
            f"**Claim.** {esc(r['claim'])}",
            "",
            f"**Source.** {esc(r['source'])}",
            "",
            f"**Where.** {esc(r['locator'])}",
            "",
            f"**Support.** {esc(r['support'])}; confidence {esc(r['confidence'])}.",
            "",
        ]
        if r["caveat"].strip():
            lines += [f"**Caveat.** {esc(r['caveat'])}", ""]
    lines += [":::", ""]
    return "\n".join(lines) + "\n"


def main():
    content = build()
    if "--check" in sys.argv:
        try:
            current = open(OUT, encoding="utf-8").read()
        except FileNotFoundError:
            current = ""
        if current != content:
            print(f"FAIL: {OUT} is stale; run python3 scripts/build_sources_page.py")
            return 1
        print(f"PASS: {OUT} matches {CSV}.")
        return 0
    open(OUT, "w", encoding="utf-8").write(content)
    print(f"Wrote {OUT}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

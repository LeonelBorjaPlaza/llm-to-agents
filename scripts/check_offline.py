#!/usr/bin/env python3
"""
Offline-dependency check for the rendered presentation artifact.

Per the approved implementation plan (decision D2), strict offline
verification in this stage applies to the PRESENTATION artifact only
(slides/llms-to-agents.html) -- not to every website page. This script
scans that one rendered file for anything that would require a live
network connection to display correctly: an external <script src>,
<link href>, <img src>, @import, or CSS url(), where "external" means an
absolute http(s):// or protocol-relative "//" URL.

A plain citation <a href="https://...">...</a> is fine and expected --
those are links a reader may or may not click, not something the browser
must fetch to render the slide. This script enumerates them separately and
does not fail on their account.

Scanning only HTML tag attributes is NOT enough: a script can construct and
inject a <script src="..."> element at runtime from a URL that only ever
appears as a plain JavaScript string literal, never as markup. Quarto's
bundled Reveal.js math plugin does exactly this for MathJax/KaTeX. So this
script also does a plain substring search across the whole file for known
CDN hostnames, independent of HTML structure.

This is a STATIC check: it inspects the HTML source for network-dependent
references. It cannot substitute for opening the file with the network
disabled in a real browser, which is the actual Stage-1 acceptance test
and must be performed by a human (see docs/build-log.md).

Usage: python3 scripts/check_offline.py [site_dir]
Exit code 0 if no disqualifying reference is found in the deck; 1 otherwise.
"""
import os
import re
import sys

DECK_RELATIVE_PATH = os.path.join("slides", "llms-to-agents.html")

EXTERNAL_RE = re.compile(r'^(https?:)?//')

TAG_ATTR_PATTERNS = [
    ("script src", re.compile(r'<script[^>]*\ssrc=["\']([^"\']+)["\']', re.IGNORECASE)),
    ("link href", re.compile(r'<link[^>]*\shref=["\']([^"\']+)["\']', re.IGNORECASE)),
    ("img src", re.compile(r'<img[^>]*\ssrc=["\']([^"\']+)["\']', re.IGNORECASE)),
]
CSS_IMPORT_RE = re.compile(r'@import\s+["\']?([^"\';)]+)', re.IGNORECASE)
CSS_URL_RE = re.compile(r'url\(\s*["\']?([^"\')]+)["\']?\s*\)', re.IGNORECASE)
ANCHOR_HREF_RE = re.compile(r'<a[^>]*\shref=["\']([^"\']+)["\']', re.IGNORECASE)

# Known CDN / third-party hosts that would require live internet access.
# Checked as a plain substring search across the ENTIRE file, including
# inside inline <script> blocks -- a script can build and inject a
# <script src="..."> element at runtime from a URL that never appears as
# markup, only as a JavaScript string literal (this is exactly what
# Quarto's bundled Reveal.js math plugin does for MathJax/KaTeX).
KNOWN_CDN_HOSTS = [
    "cdn.jsdelivr.net",
    "cdnjs.cloudflare.com",
    "unpkg.com",
    "fonts.googleapis.com",
    "fonts.gstatic.com",
    "ajax.googleapis.com",
]


def main():
    site_dir = sys.argv[1] if len(sys.argv) > 1 else "_site"
    deck_path = os.path.join(site_dir, DECK_RELATIVE_PATH)

    if not os.path.isfile(deck_path):
        print(f"FAIL: rendered deck not found at '{deck_path}'. Run `quarto render` first.")
        return 1

    with open(deck_path, "r", encoding="utf-8", errors="replace") as fh:
        text = fh.read()

    disqualifying = []

    for label, pattern in TAG_ATTR_PATTERNS:
        for match in pattern.finditer(text):
            url = match.group(1)
            if EXTERNAL_RE.match(url):
                disqualifying.append(f"{label}=\"{url}\"")

    for match in CSS_IMPORT_RE.finditer(text):
        url = match.group(1).strip()
        if EXTERNAL_RE.match(url):
            disqualifying.append(f"@import \"{url}\"")

    for match in CSS_URL_RE.finditer(text):
        url = match.group(1).strip()
        if EXTERNAL_RE.match(url):
            disqualifying.append(f"url({url})")

    citation_links = [
        m.group(1) for m in ANCHOR_HREF_RE.finditer(text) if EXTERNAL_RE.match(m.group(1))
    ]

    cdn_hits = []
    for host in KNOWN_CDN_HOSTS:
        count = text.count(host)
        if count:
            cdn_hits.append((host, count))

    print(f"Scanned '{deck_path}' ({len(text)} bytes).")
    print(f"{len(citation_links)} external citation <a href> link(s) found (allowed, not fetched to render):")
    for link in sorted(set(citation_links)):
        print(f"  - {link}")

    if cdn_hits:
        for host, count in cdn_hits:
            disqualifying.append(f"whole-file substring match: \"{host}\" appears {count} time(s) (may be inside inline JavaScript, not markup)")

    if disqualifying:
        print(f"FAIL: {len(disqualifying)} network-dependent reference(s) found in the deck:")
        for d in sorted(set(disqualifying)):
            print(f"  - {d}")
        print(
            "These would require a live network connection at presentation time. "
            "See implementation-plan decision D2: test Quarto's native "
            "embed-resources + self-contained-math, and if it cannot eliminate "
            "these, stop and report before vendoring anything."
        )
        return 1

    print("PASS (static check only): no external <script>/<link>/<img>/@import/url() reference found in the deck.")
    print("This does NOT substitute for opening the rendered deck with the network disabled in a real")
    print("browser -- that human check is still required and is tracked separately in docs/build-log.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

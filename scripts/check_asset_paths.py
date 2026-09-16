#!/usr/bin/env python3
"""
Guard against one specific regression: a rendered page referencing a site
asset with an origin-root path (src="/assets/..." or href="/assets/...").
Such a path works only when the site is served from the domain root; it
breaks under `quarto preview` sub-paths and when the site is published
under a prefix. Quarto rewrites root-relative paths it processes, but raw
HTML included after the body is not guaranteed to be rewritten, so the
glossary-preview script is inlined and this check confirms nothing else
slipped through.

Usage: python3 scripts/check_asset_paths.py [site_dir]
Exit code 0 if no origin-root asset reference is found; 1 otherwise.
"""
import os
import re
import sys

PATTERN = re.compile(r'(?:src|href)="/assets/')


def main():
    site_dir = sys.argv[1] if len(sys.argv) > 1 else "_site"
    if not os.path.isdir(site_dir):
        print(f"FAIL: '{site_dir}' does not exist. Run `quarto render` first.")
        return 1
    hits = []
    scanned = 0
    for root, _dirs, files in os.walk(site_dir):
        for f in files:
            if not f.endswith(".html"):
                continue
            path = os.path.join(root, f)
            scanned += 1
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                for n, line in enumerate(fh, 1):
                    if PATTERN.search(line):
                        hits.append(f"{os.path.relpath(path, site_dir)}:{n}")
    if hits:
        print(f"FAIL: {len(hits)} origin-root asset reference(s) (src/href=\"/assets/...\"):")
        for h in hits:
            print(f"  - {h}")
        return 1
    print(f"PASS: no origin-root asset references in {scanned} rendered page(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

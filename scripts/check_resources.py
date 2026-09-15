#!/usr/bin/env python3
"""
Check resources.qmd, the curated learning library, for the failure modes
a curated list actually has:

  * an entry missing a required field (Creator, Format, Level, Useful
    for, Limitation, Link or Links);
  * a URL listed twice;
  * a Link field with no https:// URL in it;
  * the total drifting outside the curated bound (MIN_ENTRIES to
    MAX_ENTRIES), which is the point of "curate rather than accumulate";
  * duplicate entry headings.

External URLs are not fetched here (no network at verify time); the
access date on the page records when they were last opened by a person
or a session with network access.

Usage: python3 scripts/check_resources.py [resources.qmd]
Exit code 0 if every check passes; 1 otherwise.
"""
import re
import sys

MIN_ENTRIES = 12
MAX_ENTRIES = 22
REQUIRED_FIELDS = ["Creator", "Format", "Level", "Useful for", "Limitation"]
LINK_FIELDS = ("Link", "Links")

ENTRY_RE = re.compile(r"^### (.+?)\s*$")
FIELD_RE = re.compile(r"^- \*\*([A-Za-z ]+?):\*\*")
URL_RE = re.compile(r"<(https?://[^>]+)>")


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "resources.qmd"
    with open(path, "r", encoding="utf-8") as fh:
        lines = fh.read().splitlines()

    entries = []  # (title, [lines])
    for line in lines:
        m = ENTRY_RE.match(line)
        if m:
            entries.append((m.group(1), []))
        elif entries:
            entries[-1][1].append(line)

    failures = []
    if not (MIN_ENTRIES <= len(entries) <= MAX_ENTRIES):
        failures.append(
            f"{len(entries)} entries; the curated bound is {MIN_ENTRIES}-{MAX_ENTRIES}"
        )
    titles = [t for t, _ in entries]
    for dup in sorted({t for t in titles if titles.count(t) > 1}):
        failures.append(f"duplicate entry heading '{dup}'")

    seen_urls = {}
    for title, body in entries:
        fields = {}
        current = None
        for line in body:
            m = FIELD_RE.match(line)
            if m:
                current = m.group(1)
                fields[current] = line[m.end():]
            elif current and line.startswith("  "):
                fields[current] += " " + line.strip()
        for req in REQUIRED_FIELDS:
            if req not in fields:
                failures.append(f"'{title}' is missing the field '{req}'")
        link_text = " ".join(fields.get(k, "") for k in LINK_FIELDS)
        if not any(k in fields for k in LINK_FIELDS):
            failures.append(f"'{title}' is missing a 'Link' or 'Links' field")
        urls = URL_RE.findall(link_text)
        if any(k in fields for k in LINK_FIELDS) and not urls:
            failures.append(f"'{title}' has a Link field with no <https://...> URL")
        for url in urls:
            if not url.startswith("http"):
                failures.append(f"'{title}' has a malformed URL '{url}'")
            if url in seen_urls:
                failures.append(f"URL listed twice: '{url}' ('{seen_urls[url]}' and '{title}')")
            seen_urls[url] = title

    if failures:
        print(f"FAIL: {len(failures)} resources problem(s):")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(
        f"PASS: {len(entries)} curated resources (bound {MIN_ENTRIES}-{MAX_ENTRIES}), "
        f"all required fields present, {len(seen_urls)} distinct URLs, none duplicated."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

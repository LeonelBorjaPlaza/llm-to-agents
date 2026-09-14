#!/usr/bin/env python3
"""
Check internal links and anchors in the rendered site.

Stage 1 scope only: internal links (relative paths, or paths starting with
"/") and same-document/other-document anchors ("#fragment"). External URLs
are deliberately NOT checked here -- that is a later stage's job, once the
site has more than two source citations worth batching into a networked
check.

Usage: python3 scripts/check_links.py [site_dir]
Exit code 0 if every internal link and anchor resolves; 1 otherwise.
"""
import html.parser
import os
import sys
import urllib.parse


class LinkCollector(html.parser.HTMLParser):
    """Collects every element id= and every href=/src= in one HTML file."""

    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []  # list of (attr_name, value)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs and attrs["id"]:
            self.ids.add(attrs["id"])
        # Anchor targets can also be plain <a name="...">.
        if tag == "a" and attrs.get("name"):
            self.ids.add(attrs["name"])
        for attr_name in ("href", "src"):
            if attrs.get(attr_name):
                self.links.append((attr_name, attrs[attr_name]))

    handle_startendtag = handle_starttag


def is_internal(url: str) -> bool:
    if url.startswith(("http://", "https://", "mailto:", "javascript:", "data:")):
        return False
    if url.startswith("//"):
        return False
    return True


def main():
    site_dir = sys.argv[1] if len(sys.argv) > 1 else "_site"
    if not os.path.isdir(site_dir):
        print(f"FAIL: site directory '{site_dir}' does not exist. Run `quarto render` first.")
        return 1

    html_files = []
    for root, _dirs, files in os.walk(site_dir):
        for f in files:
            if f.endswith(".html"):
                html_files.append(os.path.relpath(os.path.join(root, f), site_dir))

    if not html_files:
        print(f"FAIL: no .html files found under '{site_dir}'.")
        return 1

    ids_by_file = {}
    links_by_file = {}
    for rel_path in html_files:
        full_path = os.path.join(site_dir, rel_path)
        parser = LinkCollector()
        with open(full_path, "r", encoding="utf-8", errors="replace") as fh:
            parser.feed(fh.read())
        ids_by_file[rel_path] = parser.ids
        links_by_file[rel_path] = parser.links

    failures = []
    checked = 0

    for rel_path, links in links_by_file.items():
        base_dir = os.path.dirname(rel_path)
        for attr_name, raw_url in links:
            if not is_internal(raw_url):
                continue
            checked += 1
            parsed = urllib.parse.urlsplit(raw_url)
            target_path_part = parsed.path
            fragment = parsed.fragment

            if target_path_part == "":
                # Pure fragment link, e.g. href="#section" -- resolves
                # within the current document.
                target_rel = rel_path
            elif target_path_part.startswith("/"):
                target_rel = target_path_part.lstrip("/")
            else:
                target_rel = os.path.normpath(os.path.join(base_dir, target_path_part))

            # A link to a directory implies its index.html.
            candidate = os.path.join(site_dir, target_rel)
            if os.path.isdir(candidate):
                target_rel = os.path.join(target_rel, "index.html")

            if target_rel not in ids_by_file and not os.path.isfile(os.path.join(site_dir, target_rel)):
                failures.append(
                    f"{rel_path}: {attr_name}=\"{raw_url}\" -> target file '{target_rel}' does not exist"
                )
                continue

            if fragment:
                target_ids = ids_by_file.get(target_rel)
                if target_ids is None:
                    # Target file exists but was not one of our parsed
                    # .html files (e.g. a non-HTML asset) -- cannot check
                    # the fragment; treat as unresolvable for safety.
                    failures.append(
                        f"{rel_path}: {attr_name}=\"{raw_url}\" -> fragment target '{target_rel}' "
                        f"was not parsed as HTML, cannot verify anchor '#{fragment}'"
                    )
                elif fragment not in target_ids:
                    failures.append(
                        f"{rel_path}: {attr_name}=\"{raw_url}\" -> no element with id=\"{fragment}\" "
                        f"in '{target_rel}'"
                    )

    print(f"Checked {checked} internal link(s)/anchor(s) across {len(html_files)} file(s).")
    if failures:
        print(f"FAIL: {len(failures)} broken internal link(s):")
        for f in failures:
            print(f"  - {f}")
        return 1

    print("PASS: all internal links and anchors resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

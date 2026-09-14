#!/usr/bin/env python3
"""
Reconcile claim IDs cited in content against sources/claims.csv, in both
directions: every [S-nn] cited in a .qmd file must have a row in the CSV,
and every row in the CSV must be cited by at least one .qmd file. Either
direction failing means the source map and the content have drifted apart.

Usage: python3 scripts/check_sources.py
Exit code 0 if both directions reconcile; 1 otherwise.
"""
import csv
import glob
import re
import sys

CLAIM_PATTERN = re.compile(r"\[S-(\d+)\]")
CONTENT_GLOBS = ["learn/*.qmd", "slides/*.qmd", "index.qmd"]


def find_cited_ids():
    cited = {}  # id -> list of files citing it
    for pattern in CONTENT_GLOBS:
        for path in glob.glob(pattern):
            with open(path, "r", encoding="utf-8") as fh:
                text = fh.read()
            for match in CLAIM_PATTERN.finditer(text):
                claim_id = f"S-{match.group(1)}"
                cited.setdefault(claim_id, []).append(path)
    return cited


def read_claims_csv(path="sources/claims.csv"):
    with open(path, "r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
    ids = {row["id"] for row in rows}
    if len(ids) != len(rows):
        print("FAIL: sources/claims.csv contains duplicate claim IDs.")
        sys.exit(1)
    return ids, rows


def main():
    cited = find_cited_ids()
    cited_ids = set(cited.keys())
    csv_ids, _rows = read_claims_csv()

    orphan_citations = cited_ids - csv_ids  # cited in content, no CSV row
    unused_rows = csv_ids - cited_ids  # CSV row, never cited

    ok = True
    if orphan_citations:
        ok = False
        print(f"FAIL: {len(orphan_citations)} claim ID(s) cited in content but missing from sources/claims.csv:")
        for claim_id in sorted(orphan_citations):
            files = ", ".join(cited[claim_id])
            print(f"  - {claim_id} (cited in: {files})")

    if unused_rows:
        ok = False
        print(f"FAIL: {len(unused_rows)} row(s) in sources/claims.csv are never cited in content:")
        for claim_id in sorted(unused_rows):
            print(f"  - {claim_id}")

    if ok:
        print(f"PASS: {len(cited_ids)} claim ID(s) reconcile exactly between content and sources/claims.csv.")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())

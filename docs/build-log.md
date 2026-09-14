# Build log

## Stage 0 — Git initialization

- Date: 2026-09-14
- Requested by: external review, approved plan (Revision 3)
- Implemented with: Sonnet (post plan-mode exit)

Ran `git init` in `course-site/`. Created `.gitignore`. Committed exactly
two pre-existing files plus `.gitignore` (root commit `5870d53`):
`docs/prompts/01-research-and-plan.md` and `docs/prompts/RUN_TASK_01.md`
(both predate this session; neither is a generated artifact). No remote,
branch, or push.

## Stage 1 — Vertical slice

- Date: 2026-09-14
- Requested by: external review, approved plan (Revision 3)
- Implemented with: Sonnet
- Starting state: Stage 0 baseline commit `5870d53`

### Objective

Prove the architecture — Quarto website, Reveal.js deck, one browser
interactive with a no-JavaScript fallback, all offline-capable — on the
narrowest possible content slice: softmax, sampling, and temperature only.

### Files created

22 new files, none of them placeholders for unbuilt content:

```
CLAUDE.md                              155 lines
README.md                               82 lines
_quarto.yml                             33 lines
index.qmd                               48 lines
resources.qmd                           60 lines
learn/softmax-sampling.qmd             279 lines
slides/llms-to-agents.qmd              111 lines
slides/_deck.scss                       28 lines
_includes/_softmax-lab.qmd              94 lines
_includes/_softmax-fallback.qmd         53 lines
assets/js/prng.js                       21 lines
assets/js/softmax-lab.js               216 lines
assets/css/site.scss                    26 lines
assets/css/interactives.css            135 lines
sources/source-map.md                   49 lines
sources/claims.csv                       9 lines (8 claim rows + header)
docs/decisions.md                       15 lines
scripts/verify.sh                       63 lines
scripts/check_links.py                 137 lines
scripts/check_sources.py                72 lines
scripts/check_softmax_reference.py     129 lines
scripts/check_offline.py               133 lines
```

Plus this file. `.gitignore` gained one line (`**/*.quarto_ipynb`) between
Stage 0 and Stage 1 — that edit was not made by this session; it was
present on disk when checked and has been left as-is.

**Not created, per the approved scope:** the other five learning modules,
`glossary.qmd`, the agent-loop interactive, any tokenization component,
`sources/resources.csv`, and the Stage-2-only verification scripts.

### Commands run

```
git init
quarto render                          # twice — see "problems encountered"
python3 scripts/check_links.py
python3 scripts/check_sources.py
python3 scripts/check_softmax_reference.py
python3 scripts/check_offline.py       # rewritten once — see below
bash scripts/verify.sh
git status --short
git diff --stat
```

### Problems encountered and corrected during this stage

Recording these because they were real mistakes, not just steps taken —
consistent with reporting honestly rather than describing only the parts
that went smoothly.

1. **Broken nested include.** `_includes/_softmax-lab.qmd` included
   `_softmax-fallback.qmd` with a path relative to itself. Quarto resolves
   a nested `{{< include >}}` relative to the *outer* including document
   (`learn/softmax-sampling.qmd` or `slides/llms-to-agents.qmd`), not to
   the file doing the nested include. First render failed with "could not
   find file .../learn/_softmax-fallback.qmd". Fixed by changing the
   nested include path to `../_includes/_softmax-fallback.qmd`, which
   resolves correctly from both call sites (both are exactly one directory
   below the project root).

2. **`embed-resources`/`self-contained-math` set globally instead of on
   the deck alone.** The first working render produced `index.html` and
   `resources.html` at ~2.1 MB and `softmax-sampling.html` at 3.2 MB —
   every ordinary site page was being fully self-contained (Bootstrap,
   fonts, everything inlined), which directly contradicts the approved
   plan's explicit scope: *"For Stage 1, strict offline verification
   applies to the presentation artifact. Do not over-engineer every
   website page as a separate self-contained document."* I had put both
   options in the global `format: html:` block in `_quarto.yml` instead of
   only in the `revealjs:` block on the slide file. Fixed by removing them
   from the global block (they remain, correctly, only on
   `slides/llms-to-agents.qmd`'s own `revealjs:` front matter). After the
   fix: `index.html` 24 KB, `softmax-sampling.html` 48 KB,
   `resources.html` 28 KB — and the deck alone stays large (3.4 MB) because
   it is the one file meant to be self-contained.

3. **`check_offline.py`'s first version produced a false pass.** It only
   scanned HTML tag attributes (`<script src>`, `<link href>`, `<img src>`,
   `@import`, `url()`). Quarto's bundled Reveal.js math plugin does not
   load MathJax/KaTeX via a static `<script src>` tag — it constructs and
   injects the `<script>` element *at runtime from a JavaScript string
   literal* (`"https://cdn.jsdelivr.net/npm/katex"` etc., embedded inside
   an inlined `<script>...</script>` block). A tag-attribute scan cannot
   see that. The first run of the script reported PASS on a deck that in
   fact still depends on a CDN. Caught by manually inspecting the rendered
   HTML for `cdn.jsdelivr.net` before trusting the script's own verdict.
   Fixed by adding a whole-file substring search for known CDN hostnames,
   independent of HTML structure. The corrected script now correctly
   reports FAIL (see next section) — this is the script working as
   intended, not a new problem.

4. **The interactive was written into the module but only linked from,
   not embedded on, the sampling-and-temperature slide.** The design
   principle stated elsewhere in this project is that the deck and the
   site page render *the same* interactive component from one included
   file. The first draft of the slide only linked to
   `learn/softmax-sampling.qmd` rather than including
   `_includes/_softmax-lab.qmd` directly, so the live interactive did not
   actually appear on the slide. Fixed by adding the same
   `{{< include >}}` used on the module page; confirmed in the re-rendered
   output (`data-softmax-lab` and the `<noscript>` fallback both now
   appear in `_site/slides/llms-to-agents.html`).

### The empirical test required by decision D2, and its result

**Decision D2 required testing whether Quarto's native
`embed-resources: true` + `self-contained-math: true` eliminate the deck's
dependency on a CDN for math rendering, before considering anything else,
and required stopping and reporting the exact failure if the native route
did not work — not proceeding to vendor a library.**

**Result: the native route does not eliminate the CDN dependency, for a
documented and specific reason.**

`self-contained-math` is a Pandoc-level option (tagged `$html-files` in
Quarto's own schema) that governs Pandoc's native `--mathjax`/`--katex`
embedding for plain HTML documents. Quarto's Reveal.js output does not use
that code path at all — it uses its own bundled `RevealMath` plugin
(`reveal/plugin/math/plugin.js`), which is a separate system with its own
default behavior: dynamically construct a `<script>` element pointing at
`https://cdn.jsdelivr.net/npm/katex` (or the MathJax equivalents) and
inject it at slide-load time. `embed-resources: true` does inline that
*plugin's own JavaScript* into the single HTML file (which is why the deck
is 3.4 MB and does not reference an external plugin bundle) — but the
plugin's inlined code still runs its normal logic, which is to reach out to
the CDN for the actual math-rendering library. Neither option changes that
default.

Confirmed directly in the rendered file:
`_site/slides/llms-to-agents.html` contains `cdn.jsdelivr.net` four times,
inside inlined `<script>` blocks — not as a `<script src>` attribute, but
as a URL string the plugin's own code uses to build one at runtime. This
matches the exact failure mode the plan's own text anticipated: *"Quarto
documents that some dynamically loaded Reveal.js features may not work in
self-contained output"* — confirmed empirically rather than assumed.

`scripts/check_offline.py` (after the fix in item 3 above) reports this
correctly:

```
FAIL: 1 network-dependent reference(s) found in the deck:
  - whole-file substring match: "cdn.jsdelivr.net" appears 4 time(s)
    (may be inside inline JavaScript, not markup)
```

**Per the approved plan, this stops here.** No KaTeX vendoring and no
hand-authored equation SVG have been attempted. That choice — vendor
locally, or something else — is the reviewer's to make, informed by this
exact failure rather than by an assumption about it.

### Checks and results

| # | Check | Result |
|---|---|---|
| 1 | `quarto render` | **PASS** — 4 files render cleanly, no warnings |
| 2 | Internal links (`check_links.py`) | **PASS** — 88 internal links/anchors checked across 5 rendered HTML files, all resolve |
| 3 | Source-claim reconciliation (`check_sources.py`) | **PASS** — 8 claim IDs used in content, all 8 present in `sources/claims.csv`, no orphans either direction |
| 4 | Softmax numerical reference (`check_softmax_reference.py`) | **PASS** — the fallback table's 15 values (5 tokens × 3 temperatures) and the T=1.0 bar-chart widths all match an independent recomputation to within tolerance |
| 5 | Offline presentation check, static (`check_offline.py`) | **FAIL** — see D2 result above. This is the expected, correctly-detected outcome, not a bug in the check |
| 6 | Open the website in a browser | **SKIPPED — PENDING HUMAN.** No headless browser is installed in this environment (verified absent in the repository audit), and decision D5 forbids installing one in this stage. Requires a human to open `_site/index.html`. |
| 7 | Open the deck in a browser | **SKIPPED — PENDING HUMAN.** Same reason. Requires a human to open `_site/slides/llms-to-agents.html`. Given check #5's result, this will visibly fail to render its equations without network access — that is expected, not a surprise, once a human performs it. |
| 8 | Test the softmax interactive | **SKIPPED — PENDING HUMAN.** Requires a real browser with JavaScript enabled. The interactive was written to a numerically-stable softmax implementation and its fallback numbers are machine-verified (check #4), but its live DOM behavior (sliders, draw buttons, empirical-frequency overlay) has not been exercised in an actual browser. |
| 9 | Test the static fallback | **SKIPPED — PENDING HUMAN.** Requires disabling JavaScript in a real browser and confirming the `<noscript>` content (§9's static table and SVG bar chart) displays instead of the interactive. |
| 10 | Open the deck with no network access | **NOT MEANINGFULLY TESTABLE separately from #7** — the static check (#5) already demonstrates the deck currently *requires* network access for its equations; a human network-disabled test would confirm the same failure directly, but would not add new information beyond what #5 already shows for this specific issue. Speaker notes and navigation, which do not depend on the CDN, still need a human check with network disabled to confirm they are unaffected. |
| 11 | Speaker notes and navigation | **SKIPPED — PENDING HUMAN.** Both slides carry `::: {.notes} :::` blocks with content and per-slide timing; navigation is Reveal.js's standard arrow-key/overview behavior, unmodified. Neither has been exercised in a browser. |

### Human review

Pending. This report is being returned for external review before any
further action, per the approved plan's stop condition.

### Revisions

Three fixes made during this stage are described under "Problems
encountered" above: the nested-include path, the scope of
`embed-resources`/`self-contained-math`, and the offline-check script's
blind spot for runtime-constructed script tags.

### Final result

Stage 1 vertical slice is content-complete for its approved scope (one
standalone module, three slides, one interactive with a working fallback,
a reconciled source map) and passes every scripted check **except** the
offline presentation check, which correctly identifies a real,
plan-anticipated blocker (D2) rather than papering over it. All required
human-browser checks are outstanding and explicitly listed above, not
silently assumed to pass. Nothing has been committed beyond the Stage 0
baseline. Nothing has been installed. Nothing outside `course-site/` was
read or modified.

### Commit

Not committed. Left as an uncommitted, reviewable diff on top of baseline
commit `5870d53`, per the approved plan.

### Lessons for the course

- Reveal.js's math plugin is architecturally separate from Pandoc's own
  math-embedding options; `self-contained-math` is not a general "make the
  math offline" switch for every Quarto output format, and this should be
  written into `learn/transformers-attention.qmd` or wherever the course
  eventually discusses its own build process, since it is a good concrete
  example of "a green build is not proof of correctness" (precision rule
  PR6) — the render succeeded with no warnings, and the equations still
  would not have displayed offline.
- A static analysis of rendered HTML is not sufficient to verify "no
  network dependency" when JavaScript can construct its own requests at
  runtime; any future automated check in this repository should keep
  scanning full file contents, not just tag attributes.

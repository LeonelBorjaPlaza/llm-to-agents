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

## Redesign batch: review checkpoint, corrections, two new lessons

- Date: 2026-09-14
- Requested by: external review, approved implementation plan (bounded batch)
- Implemented with: Sonnet
- Starting state: Stage 1 checkpoint commit `c98c7dd`

### Objective

Checkpoint the Stage 1 prototype honestly; retarget the design to a
35–40 minute talk with no required live equation or demonstration and the
website as the primary product; fix a real error in `CLAUDE.md`; build two
new complete, standalone, numerically-verified lessons; write a local
prose-editing Skill; and save the remaining design as planning documents.
Leave everything past the checkpoint uncommitted.

### Files created

- `docs/reviews/stage1-first-learner-review.md`
- `learn/neural-networks.qmd` (311 lines)
- `learn/why-transformers.qmd` (218 lines)
- `scripts/check_neuron_example.py`
- `scripts/check_transformer_path_lengths.py`
- `.claude/skills/reader-first-course-editor/SKILL.md`
- `docs/live-talk-storyboard.md`
- `docs/site-architecture.md`
- `docs/milestone-timeline.md`
- `docs/practical-guide-spec.md`

### Files changed

- `CLAUDE.md` — duration 45→35–40 min; product-hierarchy strengthened
  toward site-primary; superseded-design note added; **fixed CC3**
  (removed "product-level system instructions" from the post-training
  list — it incorrectly classified inference-time context as a
  post-training method); added CC5 (backprop vs. optimizer), PR8 (logit
  terminology), PR9 (prompting qualifications), PR10 (historical claims),
  a vocabulary-hierarchy note, and a standing no-production-commentary
  rule.
- `docs/decisions.md` — nine new dated rows recording the checkpoint, the
  duration/design change, the CC3 fix, the S-01…S-08 audit result, the
  FlashAttention and R1/R1-Zero deferrals, and the Vaswani et al.
  verification.
- `learn/softmax-sampling.qmd` — pre-softmax scores introduced before the
  term "logit" (§3, rewritten in place, no section renumbering needed);
  logit/statistics-logit distinction added; softmax- and
  temperature-naming etymologies added; toy-vocabulary labeling; the
  multinomial-logit connection marked as an optional bridge; two
  production-commentary asides removed from §11. Applied the reader-first
  Skill's review procedure as a separate pass afterward — no further
  prose or meaning changes were found necessary; the pass's checks
  (`check_sources.py`, `check_softmax_reference.py`) both passed.
- `index.qmd`, `resources.qmd`, `_quarto.yml`, `README.md` — duration and
  module-count updates; navbar's `Learn` link became a three-entry
  dropdown; a new annotated Vaswani et al. entry in `resources.qmd`; the
  three existing slides reframed as a historical prototype, left
  unedited.
- `sources/claims.csv`, `sources/source-map.md` — twelve new claim rows
  (S-09…S-20); new gap G2 recorded; S-16/S-17/S-19's new Vaswani et al.
  locators marked **verified against the live paper**, distinct from the
  still-open, reused S1/S2 timestamps (gap G1, unchanged).
- `scripts/check_sources.py` — content globs widened from a hardcoded
  `index.qmd` to `*.qmd`, so any root-level page is covered automatically.
- `scripts/verify.sh` — two new steps added, renumbered 1/7…7/7.

### Commands run

```
git add <checkpoint files> && git commit   # Stage 1 checkpoint, before this batch
WebFetch https://arxiv.org/abs/1706.03762  # abstract only, insufficient
WebFetch https://arxiv.org/pdf/1706.03762  # binary; read via the PDF-aware Read tool instead
Read <fetched PDF>, pages 1-6              # confirmed Table 1, Section 1 and 3.1 text directly
quarto render                               # multiple times, during drafting
python3 scripts/check_neuron_example.py     # caught two real rounding errors, see below
python3 scripts/check_transformer_path_lengths.py  # caught one regex/line-wrap bug, see below
bash scripts/verify.sh
git status --short / git diff --stat
```

### Problems encountered and corrected during this batch

1. **A file I drafted (`docs/reviews/stage1-first-learner-review.md`) was
   reported as textually corrupted before it was ever written to disk** —
   the write was rejected before landing, confirmed by direct inspection
   (file absent). Rewrote it with plain ASCII punctuation only and less
   self-referential framing, then read it back in full to confirm no
   truncated fragments remained, per instruction.
2. **`learn/neural-networks.qmd`'s worked example had two real rounding
   errors**, caught by `scripts/check_neuron_example.py` on first run: the
   original loss was written as `≈ 1.4632`; the precise value is
   `1.463282`, which rounds to `1.4633`. The updated-parameters loss's
   intermediate `ŷ_new` was written as `0.323231`; the precise value is
   `0.323248`. Both were off by less than the script's tolerance (so the
   check technically passed either way), but were fixed to the exact
   values rather than left to rely on tolerance, since this page's whole
   point is numerical precision.
3. **`scripts/check_transformer_path_lengths.py`'s first run failed** on
   a line-wrap artifact, not a content error: the regex expected a literal
   space between "to" and "position 2," but the source `.qmd` wraps its
   markdown at that exact point. Fixed by making the regex whitespace-
   tolerant (`\s+`).
4. **Two internal cross-reference numbers in `learn/why-transformers.qmd`
   were wrong**: one pointed to "§8's misconception" when the
   misconception section is actually §10; one attributed "block
   structure" to §8 in a resource annotation when no section by that
   description exists in that file. Both fixed on a full re-read before
   moving on.

### The one licensed new-source verification

Per the approved plan's "or unresolved gaps" clause, fetched the live
Vaswani et al. paper (arXiv:1706.03762) before writing any claim citing
its Section 1, Section 3.1, or Section 4/Table 1 — these locators were
never cited anywhere in this repository before this batch. The abstract-
only fetch was insufficient; fetched the PDF directly and read it with the
PDF-aware `Read` tool. Confirmed Table 1's exact figures (Self-Attention:
$O(n^2d)$ complexity, $O(1)$ sequential operations, $O(1)$ maximum path
length; Recurrent: $O(nd^2)$, $O(n)$, $O(n)$) and Section 1's exact
sentence on recurrence precluding "parallelization within training
examples." No other source was re-verified in this batch — the reused
S1/S2 timestamps remain under the existing, unchanged gap G1.

### Checks and results

| # | Check | Result |
|---|---|---|
| 1 | `quarto render` | **PASS** — 6 files render cleanly (was 4 before this batch) |
| 2 | Internal links (`check_links.py`) | **PASS** — 177 internal links/anchors checked across 7 rendered HTML files (was 88/5) |
| 3 | Source-claim reconciliation (`check_sources.py`) | **PASS** — 20 claim IDs (S-01…S-20) reconcile exactly, both directions; content globs now cover every root `.qmd` page, not just `index.qmd` |
| 4 | Softmax numerical reference | **PASS** — unaffected by the §3 rewrite |
| 5 | Neuron/backprop numerical example (new) | **PASS** — after the two rounding fixes above |
| 6 | Transformer path-length numerical example (new) | **PASS** — after the regex fix above; confirms $O(n)$ vs. $O(1)$ growth across $n\in\{4,8,16,64\}$ |
| 7 | Offline presentation check | **FAIL — unchanged.** Reproduces exactly the same D2 finding from Stage 1; the deck was not touched by this batch, so this is confirmation of no regression, not a new problem |
| 8 | Open site/deck in a browser | **SKIPPED — PENDING HUMAN** (unchanged from Stage 1; no headless browser installed by design) |
| 9 | Exercise the interactive and its fallback | **SKIPPED — PENDING HUMAN** (unchanged) |
| 10 | Open the deck with no network access | **SKIPPED — PENDING HUMAN** (unchanged; check 7 already demonstrates the underlying failure statically) |
| 11 | Confirm speaker notes/navigation | **SKIPPED — PENDING HUMAN** (unchanged) |

### Human review

Pending. Returned for external review before any further action.

### Revisions

Four fixes made during this batch are detailed under "Problems
encountered" above.

### Final result

All batch deliverables are complete and content-real — no placeholder
pages, no empty sections. Six of seven scripted checks pass; the seventh
reproduces a known, already-diagnosed, unchanged finding. All
browser-dependent checks remain honestly reported as pending, exactly as
they were after Stage 1. Nothing was installed. Nothing outside
`course-site/` was written (the sibling coordination plan was read only,
for the practical-guide-spec provenance note).

### Commit

Not committed. Left as an uncommitted diff on top of checkpoint commit
`c98c7dd`, per instruction.

### Lessons for the course

- A numerically-verified page is only as good as the independent
  verification actually run before publishing — two real rounding errors
  in `learn/neural-networks.qmd` were within this project's own
  tolerance and would have shipped silently without the dedicated check
  script, which is exactly the case this repository's own precision rule
  PR6 warns about applied to its own production process.
- Fetching a paper's abstract page is not the same as fetching the paper;
  the arXiv abstract endpoint does not carry Table 1 or Section 4's text,
  and the PDF fetch needed the PDF-aware `Read` tool rather than the
  markdown-converting web-fetch path to be usable.

## Second first-learner review: general-reader model, jargon reduction, slide-design rules

- Date: 2026-09-14
- Requested by: external review (second first-learner review)
- Implemented with: Sonnet
- Starting state: uncommitted redesign batch on top of checkpoint `c98c7dd`

### Objective

Remove the economist/PhD audience framing everywhere in public-facing
pages and `CLAUDE.md`; adopt a general-reader model (quantitatively
capable, little or no ML vocabulary); reduce jargon and add "Think of it
this way" intuition callouts across the three existing lessons; update
the reader-first Skill to enforce all of this; and establish binding
slide-design rules declaring the Stage 1 slides style experiments, not
approved content. No new modules; no final deck.

### Files changed

- `CLAUDE.md` — replaced the "Audience and pedagogical standard" section
  with a "Reader model" section (general-reader bullets, the reminder
  rule, the jargon-reduction rule, the "Think of it this way" rule, the
  explanation standard); added a new "Slide-design rules" section;
  softened PR1's "live slide title" prescription, since it no longer
  presupposes the multinomial-logit bridge survives into the final deck.
- `.claude/skills/reader-first-course-editor/SKILL.md` — added a binding
  "Reader model" section, three new procedure steps (jargon audit,
  "Think of it this way" callouts, an aging-definitions second pass), and
  matching "Never do" entries; renumbered the remaining procedure steps
  and widened the final summary to five lists.
- `learn/softmax-sampling.qmd` — removed "a tool economists already use"
  and the PhD-specific prerequisites line; added a "Think of it this way"
  callout after logits/scores, softmax, and temperature (3 total); kept
  the multinomial-logit bridge, reframed as explicitly optional and
  conditional rather than a description of the audience.
- `learn/neural-networks.qmd` — reworked §1's opening to define $x'\beta$
  in plain language before using the notation; added six "Think of it
  this way" callouts (parameters, nonlinear activation, layers, loss,
  gradients, backpropagation); every equation block preserved
  byte-for-byte.
- `learn/why-transformers.qmd` — added a plain-language explanation of
  big-O notation before relying on it; added two "Think of it this way"
  callouts (recurrence, self-attention); reworded the arithmetic-cost
  discussion in §9 to lead with "double the input, arithmetic roughly
  quadruples" before the $O(n^2 d)$ notation.
- `index.qmd`, `README.md` — applied the exact required sentence
  replacement removing "PhD economists."
- `resources.qmd` — no audience-specific language found; unchanged in
  this pass beyond what the prior batch already did.
- `docs/decisions.md` — three new dated rows: the audience-framing
  change, the three new writing rules, and the slide-design rules.
- `docs/live-talk-storyboard.md` — added the eight-step core story
  ("training data → neural network → transformer → next-token
  prediction → training → assistant → tools → agent"), the slide-design
  rules, and an explicit note that the existing 21-segment table is
  content planning, not slide-ready wording, and will need to be
  re-screened against these rules before any future full-deck build.
- `scripts/check_transformer_path_lengths.py` — one regex made
  whitespace-tolerant across every word gap, not just one, after the
  reworded prose shifted where the source file's line wrap fell (this is
  the second time this exact class of bug has appeared; see "Lessons"
  below).

### Problems encountered and corrected during this pass

1. **Dropped a claim citation during the softmax-sampling.qmd rewrite.**
   The `[S-09]` tag (the logit-terminology claim) was not carried over
   into the rewritten §3. Caught immediately by running
   `scripts/check_sources.py` before moving on; fixed by reattaching the
   citation to the correct sentence.
2. **The transformer path-length regex broke again on a line-wrap
   shift.** Rewording §4's prose moved exactly where the paragraph wraps,
   breaking a regex that only tolerated whitespace at one specific word
   gap. Fixed by making every word gap in the pattern whitespace-tolerant,
   which should make this class of failure much less likely to recur.

### Checks and results

| # | Check | Result |
|---|---|---|
| 1 | `quarto render` | **PASS** — same 6 pages, no new warnings |
| 2 | Internal links | **PASS** — 177 links/anchors across 7 files, unchanged |
| 3 | Source-claim reconciliation | **PASS** — 20 claim IDs, both directions, after the S-09 fix above |
| 4 | Softmax numerical reference | **PASS** — unaffected by prose changes |
| 5 | Neuron/backprop numerical example | **PASS** — unaffected; every equation preserved byte-for-byte |
| 6 | Transformer path-length numerical example | **PASS** — after the regex fix above |
| 7 | Offline presentation check | **FAIL — unchanged.** Same D2 finding; deck untouched by this pass |

Spot-checked the rendered output directly: 11 "Think of it this way"
callouts render with correct Quarto callout styling across the three
lessons (3 + 6 + 2), and a repository-wide search confirms no remaining
"economist"/"PhD" reference in any public-facing page or in `CLAUDE.md`'s
audience description (the two remaining hits in `CLAUDE.md` are the
sentence announcing the change itself).

### Human review

Pending. Returned for another first-learner review, per instruction.

### Final result

All requested revisions are complete: audience framing removed from every
public-facing page and `CLAUDE.md`; jargon reduced and intuition layers
added across all three lessons without touching a single verified
equation or number; the Skill updated to enforce this going forward;
slide-design rules established, explicitly demoting the Stage 1 slides to
style experiments. Six of seven scripted checks pass; the seventh
reproduces the same known, unchanged D2 finding. Nothing committed beyond
checkpoint `c98c7dd`. Nothing installed. Nothing outside `course-site/`
touched.

### Commit

Not committed, per instruction.

### Lessons for the course

- The same class of bug (a regex anchored to one exact whitespace gap,
  broken by a later reword that shifts the line wrap) has now appeared
  twice in the same script. A regex that parses prose for verification
  purposes should default to tolerating whitespace at *every* word
  boundary it spans, not just the one gap that happened to wrap first.
- A prose-quality editing pass that touches a section carrying a claim
  citation is exactly the moment a citation is most likely to get
  silently dropped — this is precisely why the reader-first Skill's
  procedure requires running `check_sources.py` after every edit, not
  just at the end of a whole file's revision.

## Task: text-to-numbers pages (2026-09-15)

### Scope

Created `learn/how-created.qmd` (main path) and `learn/tokens-context.qmd`
(optional deep dive), per the batch instruction. The three anchor lessons
were not edited.

### Research performed (bounded)

Verified, on 2026-09-15, exactly the sentences the pages rely on:
Sennrich et al. 2016 (arXiv abstract); Radford et al. 2019, GPT-2,
Section 2.2 and the vocabulary/context sentence of Section 2.3 (PDF text
extracted with `pdftotext` after the fetch summarizer could not read the
two-column layout); Bengio et al. 2003, abstract, §1.1, §2 (PDF text);
Vaswani et al. §3.4 and the first sentence of §3.5 (arXiv HTML v7); Liu
et al. 2023 (abstract); Lewis et al. 2020 (abstract); Anthropic's
*Context windows* documentation page and the 2025-09-29 context-engineering
post (both product-specific, access-dated). No other sections of those
sources were read or cited. `learn/.Rhistory` was left untouched.

### Verification files

- `scripts/check_bpe_example.py` (new): re-runs the toy BPE merges from
  the committed word counts and checks each merge step, the final splits,
  and the context-budget subtraction against the page text. Its first run
  caught its own bug (the budget regex also matched the BPE word-count
  rows, inflating the "used" total by 18); fixed by requiring a
  plain-text label.
- `scripts/verify.sh`: added as step 7 of 8.

### Not done in this batch

- The Karpathy tokenization segment is cited as a learning resource with
  no timestamp, because none was verified.

### Correction pass before commit (2026-09-15)

Nine bounded corrections from external review, none structural: position
information made architecture-neutral (the original Transformer's added
encoding is one mechanism, not the only one); the objective named as
autoregressive pretraining; fixed tokenizer/ID mapping distinguished from
the learned embedding parameters; characters and bytes separated as
distinct base units, with subword-plus-byte-fallback described as the
common pattern rather than a universal; spaces/punctuation generalization
limited to "in many commonly used subword tokenizers ... influence the
split"; the `bank` example made causal ("the river bank" vs. "the central
bank"); the context-versus-parameters distinction separated from
product-level persistence; "re-sent" replaced with logical-context
language; and `index.qmd`'s lesson list updated so the visible path is
text → numbers → neurons → transformers, with the deep dive exposed.

## Task: attention and pretraining pages (2026-09-15, Batch 2)

### Scope

Created `learn/transformers-attention.qmd` and `learn/training.qmd`. The
five earlier lessons were not edited; no contradiction requiring an edit
to a frozen page was found.

### Research performed (bounded)

Verified on 2026-09-15: Vaswani et al. §3.2, §3.2.1 (definition and the
$\sqrt{d_k}$ paragraph), §3.2.2, §3.1, §3.3, §5.3 (arXiv HTML v7); GPT-2
§2 Equation 1, §2.3 pre-normalization sentence, and the abstract's
"begin to learn" sentence (PDF text already on disk from Batch 1);
Bengio et al. §1.1 objective sentences (PDF text); Shazeer 2019 abstract
(arXiv). The 3Blue1Brown attention lesson URL was confirmed to exist; no
timestamp is asserted. No other sources were read.

### Verification files

- `scripts/check_attention_example.py` (new): recomputes the 3-position,
  $d_k = 2$ causal example from the committed q/k/v vectors and checks
  scores, weights, masked entries, row sums, and outputs. Tables are
  located by `<!-- check:... -->` markers rather than prose.
- `scripts/check_training_example.py` (new): recomputes each $-\log p$,
  the sums and means for both models, and the two sequence-probability
  products quoted in the prose.
- `scripts/verify.sh`: both added, as steps 8 and 9 of 10.

### Choices worth recording

- The q/k/v vectors in the attention example are given as already
  projected, with the projection matrices not shown, so that the
  score → weight → weighted-sum mechanism stays visible in two-entry
  vectors.
- The training example reuses Batch 1's sentence and its four targets,
  so the shift-by-one construction is the same object across pages.
- "Like many models since" (Adam) is course characterization and is
  flagged as such in S-42's caveat.

### Correction pass before commit (2026-09-15, Batch 2)

Eleven bounded corrections from external review, none structural: the
attention opening simplified and "five positions earlier" made
non-specific; dot-product wording now notes dependence on magnitudes as
well as alignment; the incoming-representation parenthetical made
architecture-neutral about position; the objective's first-token
convention and the shift-by-one indexing reconciled in one paragraph;
the exact mini-batch gradient distinguished from its role as a noisy
estimate of the full-data gradient; "like many models since" dropped from
the Adam sentence; the trainable-parameter sentence no longer implies
every parameter gets a nonzero update; the unsupported "gradient would
push hardest" inference deleted and the four-target product named as a
conditional probability; the teleological "everything the model comes to
do" sentence replaced; "scored by nothing at all" narrowed to the
model-level statement with a one-line pointer to system-level checks; and
the head-interpretability and attention-weight cautions narrowed to what
the architecture defines. One authorized consistency edit to the
otherwise frozen `learn/tokens-context.qmd` §7: "position information is
added" became "the architecture incorporates information about position
and order", matching `learn/how-created.qmd` §6.

## Task: post-training and agents pages (2026-09-15, Batch 3)

### Scope

Created `learn/posttraining.qmd`, `learn/agents.qmd`, and the shared
include `_includes/_agent-loop.qmd` (a plain preformatted diagram, no
JavaScript, so it can be reused by the deck without an offline
dependency). The seven earlier lessons were not edited; no contradiction
requiring an edit to a frozen page was found.

### Research performed (bounded)

Verified on 2026-09-15: InstructGPT, DPO, and Constitutional AI abstracts
(arXiv abstract pages); the DeepSeek-R1 abstract and introduction (arXiv
HTML, v2), including the report's own "pure reinforcement learning"
phrase for R1-Zero and the multi-stage description of R1; Anthropic's
*Building Effective AI Agents* (article text); Anthropic's tool-use
overview page; and the Claude Code overview, skills, and permissions
pages (the permissions page was saved to disk and searched for the
permission-system table and mode list). No other sources were read.
No agent-framework survey was performed.

### Product-specific claims and access dates

All Claude API and Claude Code facts (S-51–S-54) are labeled
product-specific in the lessons and dated 2026-09-15 in `claims.csv`,
`source-map.md`, and `resources.qmd`. The lessons state the durable shape
(software executes tool requests; procedures are context; approval is
decided by software under user-controlled rules) and treat the specifics
as changeable.

### Choices worth recording

- No equations beyond one optional two-term schematic (expected reward
  minus a drift penalty) on the post-training page, explained in words.
- The DeepSeek-R1 discussion attributes "pure RL" only to R1-Zero, using
  the report's own phrase, and describes R1 with the report's verified
  "multi-stage learning framework that integrates rejection sampling,
  reinforcement learning, and supervised fine-tuning".
- The agent loop is a fenced text diagram in an include rather than a
  Mermaid or SVG figure, to avoid adding a render-time dependency in
  this batch; it can be redrawn later without changing the lesson text.

### Correction pass before commit (2026-09-15, Batch 3)

Fifteen bounded corrections from external review, none structural. Agents
page: a bare model call produces text or structured output and external
effects require surrounding software or a provider-operated tool
(replacing "producing text is all a model call does"); the tool boundary
restated as "surrounding system infrastructure interprets, executes or
routes, and supplies the result to a subsequent model step", so
provider-executed tools are covered; the workflow-versus-agent
conclusion softened to "may add cost ... without enough additional
benefit"; the loop described as the minimal mechanism behind this page's
definition rather than "the whole of what agentic means"; "fresh
invocation" replaced by architecture-neutral continuity language; "the
model learned nothing" replaced by "no model parameter was updated";
Claude Code permissions qualified as Manual-mode behavior with other
modes noted; the check answers now say the model generates the request
and the system performs the execution. Post-training page: the
comparison-cost claim made non-universal; the DPO description now says
what it removes (the separate reward model and the online RL loop) given
a fixed preference dataset; a one-sentence terminology note fixes
"classic RLHF pipeline" as this page's convention and the DPO check
question now tests mechanism; the reasoning-trace sentence now says the
policy was optimized on outcome and format rewards and the intermediate
text was not supervised as a faithful description; the pretraining
attribution softened to "many broad capabilities are established during
pretraining"; the reasoning-model misconception scoped to the DeepSeek
case; the reward schematic explicitly attached to the classic route.

## Task: practical guide and short story (2026-09-15, Batch 4)

### Scope

Created `learn/using-models-well.qmd`, `short-story.qmd`, and the shared
include `_includes/_operating-checklist.qmd` (an ordered list inside a
`.operating-checklist` div, unstyled for now, so it can be given a print
style or reused later without changing the lesson). No frozen lesson was
edited; no contradiction requiring one was found.

### Research performed (bounded)

Read on 2026-09-15: Anthropic's *Prompting best practices* (saved to disk
and searched for the examples, XML, thinking, prefill, and over-prompting
passages), OpenAI's *Prompt engineering* and *Reasoning best practices*
(the platform.openai.com URLs redirect to developers.openai.com), Google's
*Prompt design strategies*, Anthropic's *Best practices for Claude Code*,
and a targeted re-read of the context-engineering article for four
definitions. The prompt-caching sentence was taken from the
context-windows page already fetched in Batch 1. No prompt-engineering
blogs, social-media material, or listicles were consulted.

### Product-specific advice included, all access-dated 2026-09-15

- Examples in prompts: Anthropic (reliable for format), Google (always
  include), OpenAI reasoning models (try without first).
- Step-by-step instructions: OpenAI (unnecessary for reasoning models);
  Anthropic (general instruction preferred over prescriptive steps).
- Delimiters: Anthropic and OpenAI both recommend XML or Markdown
  structure.
- Prefill: Anthropic documents it as unsupported from Claude 4.6 onward.
- Snapshot pinning: OpenAI.
- Model-family choice: OpenAI's speed/cost versus accuracy/reliability
  framing.
- Claude Code: evidence over assertion, plan-before-implement,
  fresh session after repeated corrections, concise CLAUDE.md.
- Prompt caching: cached prefixes still count toward the window.

### Advice deliberately excluded

- Any universal claim about how much performance degrades with context
  length; the page cites the one empirical study and the vendor
  statements already in the course and says they are for particular
  models and dates.
- Any ranking of models by name.
- Specific "magic phrase" recommendations, role-play framings, and
  emphasis tricks; the Anthropic page's own note that emphasizing many
  lines makes none stand out was read as a reason not to teach emphasis
  as a technique.
- Percentage cost savings from caching or from any efficiency measure.
- Claude Code commands, permission modes, and subagent features beyond
  the habits they implement; the practical pages that follow will cover
  the product.

### Correction pass on the practical page (2026-09-15, Batch 4, before commit)

Eleven precision corrections to `learn/using-models-well.qmd`, none
structural: §1 no longer claims draft-task errors are cheap to see; §2
drops "plausible is what the output distribution is trained to be"; §3
replaces the "exactly three kinds of information" taxonomy with the
parameters/context/tools distinction from earlier lessons and qualifies
token cost; §6 drops the "no separate channel" sentence and keeps the
generated-assertion-versus-evidence principle; §7 no longer says
intermediate results are never seen; §8 attributes the "more than twice"
trigger explicitly to Claude Code's current guidance and states the
durable principle separately; §9 scopes every provider statement to the
document and model family that supports it (Anthropic's page covers its
current models and separates model-specific from general techniques, its
"general over prescriptive" advice sits under extended thinking with
manual chain-of-thought as the fallback; OpenAI's advice is split
between its reasoning-models guide and its general page, which says
non-reasoning GPT models perform best with explicit instructions;
Google's few-shot default is its current Gemini guidance); §10 is
restated as a heuristic with "evaluate on the actual task" and the
delegation sentence removed; §13 is risk-based, noting that reads can be
consequential and replacing the storage-only sentence; the causal-design
check answer now says "candidate for stronger or higher-effort assistance
plus human review". Claim rows S-57 and S-58 were refined to carry the
same scope. The OpenAI prompt-engineering page and the saved Anthropic
page were re-read on 2026-09-15 before editing §9; no provider claim had
to be dropped, and none contradicted the earlier reading.

### Final correction pass before commit (2026-09-15, Batch 4)

Ten precision corrections to `short-story.qmd`, none structural: token
wording made architecture-neutral; the parameter count removed and the
training sentence aligned with the training lesson (loss, gradients,
optimizer); attention described as combining information from permitted
positions (itself and earlier ones) and the why-transformers link
softened to prevalence rather than "won out"; the generation sentence no
longer implies recomputation from scratch, with a short cached key/value
note (S-43) and a decoding rule described as deterministic or
stochastic; "at each training target"; "pretraining alone does not
specifically optimize a model to behave as a conversational assistant";
context described as the request-specific information conditioned on,
with decoding settings and product logic noted and persistence stated
non-universally; the tool boundary restated in the agents lesson's
terms with provider infrastructure covered; "agent" scoped to this
course's usage; and the closing responsibility paragraph rewritten so
that models and tools assist judgment while evidence, review, and human
accountability remain necessary. One quiz answer in
`learn/using-models-well.qmd` (§15, repeated corrections) now presents
the "more than twice" threshold as a heuristic. Rendered body of the
short story measures roughly 1,500 words of main-content text plus the diagram, an 8–10 minute read.

## Task: reference layer and site consolidation (2026-09-15, Batch 5)

### Scope

Created `milestones.qmd`, `glossary.qmd`, `_includes/_milestone-rail.qmd`,
`scripts/check_glossary.py`, and `scripts/check_resources.py`; rewrote
`resources.qmd` as a curated library; reorganized `_quarto.yml`'s navbar
and `index.qmd` into Start / Learn / Deep dives / Reference tiers;
appended reference-layer CSS to `assets/css/site.scss`; added claim rows
S-64–S-74 and source entries S33–S41 to `sources/`; registered the two
new checks in `scripts/verify.sh` (now 12 steps). No frozen lesson was
edited; no contradiction requiring one was found.

### Research performed (bounded)

Primary sources opened on 2026-09-15 for the timeline: the Nature
abstract page for Rumelhart, Hinton, and Williams (1986); the
author-hosted PDF of Hochreiter and Schmidhuber (1997); the arXiv
abstract pages for Sutskever et al. (2014), Bahdanau et al. (2014/15),
Christiano et al. (2017), Wei et al. (2022), Yao et al. (2022), and
Mikolov et al. (2013, checked and then omitted); the OpenAI GPT (2018)
PDF and the BERT v1 PDF (to anchor the GPT year). Rosenblatt (1958)
could not be opened in full text (publisher wall; no open copy reachable
programmatically); its bibliographic record was verified via Crossref
and PubMed and the page cites it without quotation. For the resources
page, every listed URL was opened; stated dates, chapter counts,
prerequisites, and caveats were read from each page, and durations are
given only for the one resource (Karpathy's *Zero to Hero*) whose page
states them. The *Building effective agents* article was re-opened and
its new dated note recorded (S-73).

### Selection decisions

Milestones included (17): perceptron; backpropagation 1986; LSTM;
neural probabilistic LM; seq2seq; attention for translation; subword
units; the Transformer; pretraining and transfer (GPT, BERT, GPT-2 as
one entry); scale and in-context behavior (scaling laws and GPT-3 as one
entry); retrieval-augmented generation; chain-of-thought prompting;
InstructGPT with Christiano et al. as antecedent; ReAct; DPO; the
workflow/agent article; DeepSeek-R1. Considered and omitted: word2vec
(the course's embedding story rests on Bengio 2003), AlexNet and GPU
history, convolutional sequence models, FlashAttention and
attention alternatives, open-weight model families, product launches.

Resources retained (19) and removed from the previous 25-entry list:
BERT, scaling laws, GPT-3, Sennrich, GPT-2, Liu et al., Lewis et al.,
Shazeer, Constitutional AI, the tool-use and context-windows API pages
(all remain in the source map and lesson "Continue learning" sections);
the three provider prompting pages were folded into one entry and the
Claude Code pages into one entry. Added: 3Blue1Brown's neural-networks
series, Nielsen's book, Karpathy's *Zero to Hero*, Alammar's illustrated
posts, the Hugging Face LLM and Agents courses, Lilian Weng's 2023 agent
survey, and Stanford CS224N.

### Verification (see the run recorded below)

`bash scripts/verify.sh`: steps 1–11 pass; step 12 (offline deck check)
fails on the pre-existing `cdn.jsdelivr.net` reference in the prototype
deck, a known non-blocker carried forward unchanged. The root-level
citation coverage of `scripts/check_sources.py` was confirmed by
inspection (its `*.qmd` glob) and by a temporary negative test: an
unregistered claim ID placed in `milestones.qmd` made the check fail and
was then removed. Human-browser checks (navbar menus, glossary A–Z row,
milestone rail rendering, print view) are pending a human with a
browser.

### Final correction pass before commit (2026-09-15, Batch 5)

Precision and housekeeping corrections only; structure unchanged
(17 milestones, 98 glossary entries, 19 resources). Milestones: the
Rosenblatt entry was **narrowed** to what the title and the 1986
abstract support (a hypothetical learning system; the
perceptron-convergence procedure as an earlier learning method), after
a second attempt to reach the full text failed (academia.edu and
ResearchGate require login; the MIT Press reprint and Semantic Scholar
pages returned 403); its earlier weight-adjustment description was
dropped, and S-64 rewritten accordingly. "Routine use" (1986) replaced by
"predates the Transformer by more than three decades"; Sennrich no
longer presented as the origin of current tokenization; "the
architecture inside current LLMs" replaced by "dominant foundation for
many modern LLMs" on both the timeline and the glossary; "established
the practice" (2018–19) and "capability came from scale and data as
much as architecture" (2020) replaced by non-exclusive statements; the
Lewis entry now distinguishes the 2020 architecture from retrieval in
general; ReAct is "closely resembles", not "is"; the Anthropic 2024
entry no longer claims wide adoption; DeepSeek-R1 is "a detailed,
high-profile public case", not "the case that established". All
retrieval and provenance commentary (paywalls, undated PDFs, copies
"verified for this course") was moved off the public page into
`sources/source-map.md` and this log; the GPT 2018 year remains anchored
by the BERT v1 citation, recorded in S-69. Glossary: eleven definitions
tightened (big-O as order of growth; BPE; compaction versus handoff;
context window wording made product-neutral; feed-forward ordering not
universal; gradient descent stated as the negative-gradient step;
inference no longer says everything request-specific arrives via
context; neural network and pretraining say "trainable parameters
adjusted/updated"; pretraining objective stated exactly; prompt caching
scoped to a provider feature; transformer prevalence softened).
Resources: superlatives replaced by defensible wording; the InstructGPT
result stated as the paper's own comparison; the DPO and DeepSeek
descriptions narrowed; the public timestamp-debt sentence removed (the
debt stays as G1 in the source map); the trailing changelog paragraph
removed (its content is recorded in the Batch 5 entry above).
`README.md` updated to the current site structure and render/preview
commands.

## Task: Spine + Visual Pass (2026-09-15, after commit d8600d0)

### Scope

Rebuilt `short-story.qmd` as the definitive conceptual spine (13 numbered
sections plus an opening that states the governing question and shows
the whole lifecycle); created six reusable figures in `_includes/`
(`_fig-lifecycle.qmd`, `_fig-runnable-model.qmd`, `_fig-tiny-network.qmd`,
`_fig-rnn-vs-transformer.qmd`, `_fig-training-stages.qmd`,
`_fig-three-stores.qmd`; the agent loop is reused); added a five-category
semantic palette and figure, callout, summary, tooltip, and home-page
styles to `assets/css/site.scss`; added glossary previews
(a small script loaded site-wide through `_includes/_glossary-preview.html`
and `_quarto.yml`'s `include-after-body`; originally an external file in
`assets/js/`, inlined in the final visual pass so that it needs no asset
path); added `_includes/_one-minute-version.qmd` and a
"The one-minute version" section at the top of
`learn/using-models-well.qmd`; added a compact corpus subsection to §1 of
`learn/how-created.qmd`; linked the first important occurrence of 39 key
terms on the seven main-path pages to the glossary with no wording
changes (the neural-networks lesson keeps its CRLF line endings); put the
lifecycle figure and palette-coded tier rules on the home page; added a
video-first route and three resource entries (Karpathy 2023, Seitz with
Mody, CS336), bringing the library to 22, the configured maximum; added
claim rows S-75–S-81 and source entries S42–S46. No deep-dive page was
edited. Nothing committed.

### Short Story structure before and after

Before (10 sections): you type text → vectors enter a neural network →
the transformer → scores → why the probabilities are good → assistant →
context → tools → the loop → mental model.

After: the question this course answers (with the lifecycle figure) →
1 what the finished object is → 2 the basic computation → 3 the corpus →
4 text becomes numbers → 5 recurrent networks to the transformer →
6 pretraining makes the base model → 7 post-training makes the
assistant → 8 fluency, abstention, and evidence → 9 reasoning-oriented
RL → 10 what happens when you type → 11 parameters, context, and
external state → 12 tools and the agent loop → 13 the mental model.

### Research and what was verified

Karpathy 2023 (*Intro to Large Language Models*): official description
and chapter list verified from the video page's own data; the linked
slides are behind a login wall; the spoken "two files / 140 GB / 500
lines of C" passage exists only in a third-party transcript and is not
stated on the site (the site cites the code-plus-parameters framing to
the "LLM Inference" chapter and the description's linked ~1000-line
runner). Karpathy 2025 (*Deep Dive*): official description and chapter
list verified; no transcript obtainable; the classroom analogy is
verified verbatim from Karpathy's own 2025-01-30 post; the memory
analogy's "working memory" phrase is confirmed by the official chapter
title and by the 2023 description, while "vague recollection" is
third-party only and is paraphrased. CS336, the UW CSE 163 lesson, the
Seitz videos (via oEmbed, RSS, and an archived page; live YouTube pages
blocked), Jay Mody's post, and FineWeb (arXiv abstract plus the dataset
card's raw README) verified on 2026-09-15. MIT 6.S191 was evaluated and
not added (no lecture specifically on language models in its 2026
offering).

### Verification (this pass)

`bash scripts/verify.sh`: steps 1–11 pass; step 12 (offline deck) fails
on the pre-existing CDN reference, unchanged. Internal links: 1,086
checked, all resolve, including every glossary anchor linked from the
short story and lessons. The preview script's assumptions were mirrored
in Python against the rendered glossary: all 54 distinct glossary ids
linked site-wide have a `section.level3` with an `h3` and a first `p`.
**Browser checks not performed** (no browser in this environment): the
hover and keyboard-focus previews, the click-through, the no-JavaScript
fallback, figure legibility at laptop and phone widths, the home page,
and the rail remain release QA for a human.

### Correction pass on the Spine + Visual Pass (2026-09-15, before commit)

Precision and consistency corrections only; structure unchanged.
Short story: parameter count stated as a large learned collection
("modern large models contain billions"), not a definition; the
code-plus-checkpoint picture now cites the `llama2.c` README (S-82) as
direct support, with the 2023 talk kept as pedagogical attribution, no
runner line count, and "everything the model knows" replaced by
"the information the model learned during training is distributed across
them"; corpus disclosure stated as "often not publicly disclosed, varies
across models and providers" (same fix in `learn/how-created.qmd` §1);
recurrent networks "became established and highly influential
approaches"; backpropagation "computes the gradient of the loss with
respect to the trainable parameters"; "training code is known and
short" replaced by "architecture and optimization procedure are
specified in code; training discovers the parameter values"; base model
"not specifically optimized to behave as a conversational assistant";
post-training data stated for published recipes with Constitutional AI
and DeepSeek-R1 as examples; "smaller" data replaced by "more targeted
data and feedback"; the hallucination section restated as a careful
sequence (pretraining does not verify truth; post-training makes
question-answering more likely; a well-formed answer can outrun
parametric information; recipes can encourage abstention, calibration,
truthfulness, or tool use; post-training did not create the possibility
of unsupported answers); retrieval described as grounding in inspectable
evidence that still has to be evaluated, with "deserves more trust"
removed; reasoning RL described as checkable outcomes supplying reward
without a learned reward model for that component; decoding described as
deterministic or stochastic, with sampling as one reason for run-to-run
variation; context and persistence stated product-neutrally; the memory
analogy attributes only "working memory" to Karpathy and marks the
long-term-recall half as the course's own analogy; the mental model and
the opening use "request-specific information the model conditions on"
plus the decoding-and-product-logic clause. Consistency edits authorized
for this round: `learn/why-transformers.qmd` §1's big-O sentence now
reads "on the order of the input size" and "bounded by a constant",
matching the glossary; `learn/training.qmd` §8 now says "updating the
model's trainable parameters". Reading-time references to the short
story updated from ten to fifteen minutes in `index.qmd`, `README.md`,
and the prerequisites note of `learn/using-models-well.qmd`; historical
log entries left as written. Resources: "strongest", "fastest", and
"shortest" replaced by "recommended", "compact", and "short". A full
review patch including the untracked new files was written to
`/tmp/spine-visual-pass-full.patch` using `git add -N` followed by
`git reset`; nothing staged or committed.

### Final visual-and-interaction correction pass (2026-09-15, before commit)

Fixes from external review of the full patch, including direct
rendering of the new SVGs. RNN-versus-transformer figure: the
direction sentence now reads "information from token 1 reaches token 5
only through 4 sequential steps"; the attention arcs were moved beneath
the position boxes so no arc crosses a heading; the parallelism note is
scoped to training on a known sequence; viewBox 640×330 → 640×420.
Runnable-model figure: viewBox 640×300 → 720×340, wider boxes, smaller
headings, "billions of them, stored as a checkpoint" → "learned values
stored in a checkpoint", inference line split in two. Tiny-network
figure: viewBox 640×230 → 680×230, labels shortened to "inputs /
learned W, b / nonlinearity / output", note "in this toy unit, training
changes W and b", caption "A basic neural-network building block" with
"Larger networks combine many learned transformations and nonlinear
operations". Three-stores figure: viewBox 640×300 → 800×330, all labels
moved inside their boxes, context box relabeled "context: tokens
supplied for this step", aria and caption wording made product-neutral.
Training-stages figure: "the model's trainable parameters θ",
"an instruction-tuned, post-trained model", "use preference or reward
signals to further shape behavior", "a further post-trained model", and
a caption sentence that not every deployed model passes through exactly
these steps. Lifecycle: "assistant model" → "post-trained model", and
the single green stage split into "inference-time context" (context
color) and "tools, external state, and the loop" (system color), with
the caption stating that retrieval brings information into the context.
Narrow-width CSS: each lifecycle `li` is now a column so the stage and
its downward arrow stack. Short story: opening says post-training
shapes "a post-trained, assistant-oriented model, around which a
product builds the assistant"; §7 retitled "Post-training shapes
assistant behavior"; two "assistant model" phrases → "post-trained
model"; §2 says larger networks combine many learned transformations
and nonlinear operations; §5 scopes parallel computation to training on
a known sequence. Glossary previews: the script is now inlined in
`_includes/_glossary-preview.html` (external `assets/js/` file removed)
so it needs no asset path at any page depth or site sub-path; keyboard
focus previews no longer depend on hover capability (mouse listeners
are conditional on `(hover: hover)`, focus after a touch tap is ignored
via pointer type, keyboard focus always previews); the tooltip clamps
left and right, flips above the term when there is no room below, and
repositions on resize as well as scroll; helper text "Open glossary:
click the term or press Enter". Added `scripts/check_asset_paths.py`
(fails on any `src`/`href="/assets/"` in rendered pages) as verify step
12 of 13. A conservative static text-extent check (0.56 em per glyph,
0.6 em bold, run from the scratchpad) reports no label leaving its box
or the viewBox and no arc crossing a text band; this is not a
substitute for browser QA. The stray review artifact
`spine-visual-pass.patch` was deleted from the repository root.

## Task: reader-first and visual completion pass on the Short Story (2026-09-15, before the freeze)

### Scope

Rewrote `short-story.qmd` (13 sections plus the opening; about 4,100
words of prose, roughly a twenty-minute read) to the reader-first
standard, and completed its figure sequence. New includes:
`_fig-data-pipeline.qmd`, `_fig-token-to-vector.qmd`,
`_fig-attention-intuition.qmd`, `_fig-reasoning-compute.qmd`,
`_fig-inference-loop.qmd`, `_fig-tool-roundtrip.qmd`, and
`_fig-agent-loop.qmd` (a captioned wrapper around the existing
`_agent-loop.qmd`). Every figure now carries a stable `fig-*` wrapper
id; `scripts/check_short_story_figures.py` (verify step 13 of 14) fails
if any of the thirteen required ids is missing from the rendered page,
if they render out of narrative order, or if a `_fig-*.qmd` include is
unused. Added `.fig-rows` styles for the reasoning figure. Reading-time
references updated from fifteen to twenty minutes in the subtitle,
`index.qmd`, `README.md`, and the prerequisites note of
`learn/using-models-well.qmd`. Review artifacts removed from the
repository root. No lesson prose was edited.

### Section order after revision

The question (opening answer plus the lifecycle figure) → 1 What the
finished object is → 2 The smallest piece of a neural network → 3
Assembling the text the model learns from → 4 From text to tokens to
vectors → 5 From recurrent networks to the transformer → 6 Pretraining
makes the base model → 7 Post-training shapes assistant behavior → 8
Fluency, abstention, and evidence → 9 Reasoning-oriented models:
training, and thinking longer at inference → 10 What happens when you
type → 11 Parameters, context, and external state → 12 Tools, and the
loop that makes an agentic system → 13 The mental model.

### Research

Reasoning-model inference mechanics verified on 2026-09-15 against
Anthropic's current Thinking, Effort, Extended thinking, and Steering
thinking pages plus the 2025 announcement; Google's Gemini thinking page
(dated 2026-09-09 by the page); and OpenAI's Reasoning models page (the
platform.openai.com URL redirects to developers.openai.com). All three
describe reasoning generated before the answer, a control for how much,
and reasoning tokens counted and billed like output; all three return at
most a summary rather than the raw reasoning; Anthropic and OpenAI
describe interleaving with tool calls; only Anthropic's 2025
announcement makes an explicit faithfulness statement. The site names no
parameter and generalizes only the shared shape (S-83–S-85). Anthropic's
current pages document the 2025 budget-based mode as deprecated in
favor of adaptive thinking with an effort setting, which is why the site
says "a reasoning-effort setting or a thinking level" and nothing more
specific.

### Static figure checks

The scratchpad text-extent check (0.56 em per glyph, 0.6 em bold, 6 px
padding) reports no label leaving its box or the viewBox in any of the
eight SVG figures; the row-based figures (lifecycle, data pipeline,
reasoning, training stages) are responsive HTML. This is not a
substitute for browser QA, which remains pending for the home page, the
Short Story and its thirteen figures at laptop and phone widths, the
glossary previews, the video-first route, and the one-minute summary.

## Task: Batch 6, live deck, speaking guide, and publication preparation (2026-09-15)

### Checkpoint

Verified the pre-batch state (13 of 14 checks passing; the prototype's
CDN dependency the only failure), staged an explicit list of 36 project
files (no `learn/.Rhistory`, no patches, no generated output), scanned
the staged diff for credentials and private identifiers (none), and
committed `cd65eb6 Checkpoint website before live deck production`.
Everything below is uncommitted.

### Deliverables

`slides/llms-to-agents.qmd` (Reveal.js, 1280×720, 25 slides, no math
plugin, no CDN references); `slides/speaking-guide.qmd` (HTML, one
section per slide, timings summing to 38.0 estimated minutes, a
running-late note); `assets/css/slides.scss` (palette, chips, cards,
figure scaling, footers); nine slide figure variants
`_includes/_slide-fig-*.qmd` (tiny network without caption, RNN row,
transformer row, token lookup, training stages, attention with five
tokens, three stores, inference loop, runnable model) with larger type;
`scripts/check_slides_guide.py` (verify step 14 of 15);
`.github/workflows/publish.yml` (manual trigger; Quarto 1.10.18; checks;
Pages artifact upload and deploy); `docs/release-readiness.md`. The old
`slides/_deck.scss` was removed. Navigation: "Presentation" replaces
"Slides (prototype)"; "Speaking guide" sits under Reference; Home and
README carry one working-draft notice.

### Two site-wide defects found by browser QA and fixed

1. Every SVG figure on the website was invisible: Pandoc split the raw
   `<svg>` blocks at internal blank lines, wrapped the remainder in
   paragraphs, and the browser closed the SVG early (the rendered HTML
   read `</svg><p><desc>`). The ID-only figure check had passed. Fix: all
   figure includes are wrapped in ```` ```{=html} ```` fences, and
   `scripts/check_short_story_figures.py` now fails on a `<p>` inside an
   `<svg>` or a leaked `<desc>`.
2. The site stylesheet was never loaded: `_quarto.yml` passed
   `assets/css/site.scss` through the `css:` option, which Quarto does
   not link. Fix: `theme: [cosmo, assets/css/site.scss]`, which compiles
   the file into the theme. Chips, callouts, check-understanding boxes,
   claim-id styling, and tooltips are now styled on every page.

### Browser QA performed (headless Chromium via Playwright)

Tooling: a Playwright virtualenv in the session scratchpad, Chromium
from Playwright's official distribution, and `alsa-lib` installed through
the existing user-space Homebrew to satisfy the browser's one missing
shared library. Checks: every slide screenshotted at 1280×720 with
overflow, word-count, and minimum-font measurements (four overflows found
and fixed by slide figure variants and shorter text; none remain); the
site served at the root and under `/course-prefix/` (Home, Short Story,
`learn/agents`, glossary, deck, guide: no failed requests, no 4xx/5xx,
eight visible SVG figures on the Short Story); glossary previews on
hover, on keyboard focus, hidden on mouse-leave and Escape, click
navigating to the right anchor, at both paths; phone-width viewport with
no horizontal overflow; PDF export of the deck through Reveal's print
view (25 pages, one page rasterized and inspected). Screenshots are in
the session scratchpad, not the repository.

### Verification

`bash scripts/verify.sh`: all 15 steps pass, including the static
offline check of the new deck. `dist/course-preview.zip` (rendered site
only) and `dist/llms-to-agents.pdf` were produced; `dist/` is ignored by
Git. Not tested: opening the deck from disk with the network disabled;
every PDF page; assistive technology; the workflow itself (no remote).

## Task: publication as a public review draft (2026-09-16)

Owner-authorized destination: LeonelBorjaPlaza/llm-to-agents, public.
Before publishing, the bounded release corrections were applied (the
attention slide and guide share the bridge example; R1-Zero described as
reinforcement learning on the pretrained base model with no supervised
warm-up; exposed reasoning described as product-dependent; "training sets
every weight" softened; long links wrap at phone width), the workflow
now runs the complete `scripts/verify.sh`, claim markers render as links
to a generated public Sources page (`sources.qmd`, from `claims.csv`, via
`filters/course-links.lua`, with `build_sources_page.py --check` as
verify step 15 of 16), lesson page references render as real links, and
Home carries the review notice with a "Suggest a correction" link to the
repository's issues. History scan before the push: no deleted files, no
secret-pattern hits, no unexpected tracked paths; `learn/.Rhistory`
untracked. Commit `fc3b823` pushed; Pages enabled with build type
"workflow" through the API; run 35056786998 succeeded (build and
deploy); live checks as recorded in `docs/release-readiness.md`. Editorial
backlog recorded there: the Short Story could still be more intuitive,
more naturally written, and simpler without losing precision.

## Task: 30-minute release-candidate pass (2026-09-16, after commit 72850bf)

Owner's instruction: one bounded pass to fit the talk into a 30-minute
slot and apply a fixed list of corrections; no general style revision;
one local commit; no push or publication.

### Corrections applied

- Timing: the guide was rewritten to 28.0 prepared minutes across 24
  slides plus a 2-minute reserve (per-slide "Time: about N min (running
  total M)" lines). The product slide became a backup slide after the
  closing slide (`{#product .backup}`, on-slide label, "Time: backup");
  the runnable-model slide gained one sentence on the software around the
  model. `check_slides_guide.py` now recognizes `.backup`, requires
  backup slides after the prepared route, sums prepared minutes to 28.0,
  checks each running total, and requires the reserve and the 30-minute
  slot to be stated.
- Order: the inference-loop slide moved before reasoning-training in the
  deck and guide; Short Story §9 and §10 swapped (with the required-order
  list in `check_short_story_figures.py` updated), and their openings
  rewritten so each section stands where it now sits.
- Memorization: Carlini et al. (2021) verified and added as S-87; the
  base-model slide footer, its notes, and Short Story §6 cite it.
- Attention explanation completed (query, key, score, softmax, value,
  weighted combination) in the Short Story and the attention slide;
  figure label moved below the updated-representation box; value vectors
  defined in the caption.
- Selective wording: hardware sentence in Short Story §5 no longer says
  "should be restrained"; the announcing intro paragraph removed; §8
  closes on "Fluency is not evidence, and evidence beats confidence";
  reasoning visibility qualified in the story, slide, and guide; R1-Zero
  wording made explicit; the 2003 sentence removed from the recurrence
  slide; notes trimmed.
- Figures and CSS: tiny-network caption in HTML italics instead of TeX;
  token-to-vector label and caption quote `␣bank` as code; slide chip,
  card, legend, and step text enlarged; `.figure-tall` cap raised.
- Public wording: Home, README, and the deck's closing slide say
  30 minutes and "24 slides in the prepared route plus one backup slide".

### Defect found during browser inspection

The backup product slide rendered its last chip as inline text broken
across two lines. Cause: the product box was a bare HTML `<div>` in the
deck, and Pandoc's `markdown_in_html_blocks` behavior parsed the spans
inside it as a paragraph. The same applied to the tokens chip row (a
stray `<p>` inside `.chips`) and, harmlessly, to three lifecycle lists.
All hand-written HTML blocks in the deck are now wrapped in `{=html}`
fences, matching the figure includes. The tool-call step grid had been
fenced earlier in the pass for the same reason (typographic quotes in
code).

### Verification

`bash scripts/verify.sh`: all 16 steps pass. Deck QA in headless
Chromium: 25 sections, no overflow, minimum 16.9 px footers, 28 px body;
nine affected slides inspected from screenshots. Site QA: corrected
figures and moved anchors confirmed, glossary previews and sub-path
serving unchanged, 390 px without horizontal overflow, MathJax equations
rendered on a lesson page. `dist/llms-to-agents.pdf` regenerated
(25 pages). Not done: a timed rehearsal; inspection of every PDF page.
Committed locally as one commit; not pushed. The live site still serves
`72850bf` until the publish workflow is run.

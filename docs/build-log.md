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

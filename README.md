# From LLMs to Agents — course site

**Public working draft for review:**
<https://leonelborjaplaza.github.io/llm-to-agents/> ·
[presentation](https://leonelborjaplaza.github.io/llm-to-agents/slides/llms-to-agents.html) ·
[speaking guide](https://leonelborjaplaza.github.io/llm-to-agents/slides/speaking-guide.html).
Feedback on clarity, examples, diagrams, and factual errors is welcome
through the [issues page](https://github.com/LeonelBorjaPlaza/llm-to-agents/issues).

A Quarto website and Reveal.js deck supporting a 30-minute conceptual talk
and a standalone learning resource for readers who are comfortable following
mathematical ideas but may not use them every day: *From LLMs to agents: what
the model is, how it is built, and how it begins to act.*

This material is co-produced with Claude Code under human review. Claude Code
drafts and verifies; a human reviewer approves substantive choices, final
wording, and every commit.

## Status

**Working draft: the website, the live presentation, and its speaking
guide all exist and render; wording and figures remain under review.**
The website is the primary product; the live talk is a carefully selected,
lower-math path through it, with no required live equation or
demonstration (see `CLAUDE.md`'s product-hierarchy note).

Currently present:

- **Start:** `index.qmd` and `short-story.qmd` (the whole course in about
  twenty minutes, with a link into the lesson that develops each step);
- **Learn**, the main path in order: `learn/how-created.qmd`,
  `learn/neural-networks.qmd`, `learn/why-transformers.qmd`,
  `learn/training.qmd`, `learn/posttraining.qmd`, `learn/agents.qmd`,
  `learn/using-models-well.qmd`;
- **Deep dives**, optional technical pages: `learn/tokens-context.qmd`,
  `learn/transformers-attention.qmd`, `learn/softmax-sampling.qmd` (the
  last includes a softmax-and-sampling laboratory with a no-JavaScript
  fallback);
- **Reference:** `milestones.qmd` (a selective timeline), `glossary.qmd`,
  and `resources.qmd` (a curated learning library, distinct from the
  evidence ledger in `sources/`);
- **Presentation:** `slides/llms-to-agents.qmd` (a 30-minute Reveal.js
  deck: 24 slides in the prepared route plus one backup slide) and
  `slides/speaking-guide.qmd` (an HTML presenter guide, one section per
  slide, 28 minutes of prepared material plus a 2-minute reserve); the earlier three-slide
  prototype is preserved only in Git history;
- a source map and claim ledger (`sources/`) covering every cited claim;
- a small local editing Skill (`.claude/skills/reader-first-course-editor/`)
  for prose polishing that preserves technical meaning and claim IDs.

Known limitations are recorded in `docs/release-readiness.md`. See
`docs/site-architecture.md` and `docs/decisions.md` for the design record.

## Building

Requires [Quarto](https://quarto.org) (tested with 1.10.18). No other runtime
dependency — the plain markdown engine is used throughout; no R, Python, or
Jupyter code cells are executed at render time.

```bash
cd /projects/from-tokens-to-agents/course-site
quarto render      # build the site and deck to _site/
quarto preview     # serve the site locally with live reload
```

## Publishing an update

The site is published from this repository by a manually triggered GitHub
Actions workflow (`.github/workflows/publish.yml`), which renders the site,
runs the complete verification suite, and deploys `_site/` through the
GitHub Pages artifact flow. To publish a change:

```
edit → bash scripts/verify.sh → git commit → git push origin main
      → gh workflow run publish.yml --repo LeonelBorjaPlaza/llm-to-agents --ref main
```

Nothing is deployed automatically on push. See `docs/release-readiness.md`
for the deployment record.

Output goes to `_site/` (gitignored). Open `_site/index.html` or
`_site/slides/llms-to-agents.html` in a browser.

## Verifying

```bash
bash scripts/verify.sh
```

Runs, in order: a full render, an internal-link and anchor check, a
source-claim reconciliation check (covering every root-level and `learn/`
page), six numerical checks of the worked examples, a glossary structure
check, a curated-resources check, and an offline-dependency check on the
rendered slide output. See `docs/build-log.md` for the most recent run's
results, including any check that requires a human with a real browser
(this environment has no headless browser installed, by design).

## Repository layout

```
_quarto.yml              website + deck project configuration
index.qmd                site home page (Start / Learn / Deep dives / Reference)
short-story.qmd          the whole course in about twenty minutes
milestones.qmd           selective timeline (reference)
glossary.qmd             term reference, alphabetical with stable anchors
resources.qmd            curated learning library (reference)
learn/                    seven main-path lessons and three optional deep dives
slides/                   the Reveal.js presentation and its HTML speaking guide
_includes/                shared markup: interactive, agent loop, checklist, milestone rail, course figures
assets/                   CSS and JavaScript (vanilla, no build step)
sources/                  source map and machine-checkable claim ledger
scripts/                  verification scripts (see scripts/verify.sh)
docs/                     planning prompt, decisions, build log, reviews, and design docs
.claude/skills/           local project Skill for reader-first lesson editing
```

## Sources and claims

Every substantive factual claim on the site carries a claim ID (e.g.
`[S-01]`) that resolves in `sources/claims.csv` and is described in prose in
`sources/source-map.md`. `scripts/check_sources.py` checks this
mechanically in both directions: no claim ID without a source, and no unused
source row.

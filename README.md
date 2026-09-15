# From LLMs to Agents — course site

A Quarto website and Reveal.js deck supporting a 35–40 minute conceptual talk
and a standalone learning resource for readers who are comfortable following
mathematical ideas but may not use them every day: *From LLMs to agents: what
the model is, how it is built, and how it begins to act.*

This material is co-produced with Claude Code under human review. Claude Code
drafts and verifies; a human reviewer approves substantive choices, final
wording, and every commit.

## Status

**This site is still under construction, not the finished course.** The
website is the primary, standalone learning product; the live talk is a
carefully selected, lower-math path through it, with no required live
equation or demonstration (see `CLAUDE.md`'s product-hierarchy note).

Currently present:

- a minimal site shell (`index.qmd`, `resources.qmd`);
- three complete, standalone learning modules (`learn/softmax-sampling.qmd`,
  `learn/neural-networks.qmd`, `learn/why-transformers.qmd`);
- three slides from an earlier prototype iteration of the talk design,
  covering logits/softmax, training/maximum likelihood, and
  sampling/temperature (`slides/llms-to-agents.qmd`) — left as a historical
  checkpoint, not rebuilt to the current talk design in this batch;
- one interactive (a softmax-and-sampling laboratory) with a no-JavaScript
  fallback;
- a source map and claim ledger (`sources/`) covering the sources used so
  far;
- a small local editing Skill (`.claude/skills/reader-first-course-editor/`)
  for prose polishing that preserves technical meaning and claim IDs.

Not yet built: the remaining learning modules, the glossary, the full talk,
the agent-loop interactive, and the full curated resource library. See
`docs/prompts/01-research-and-plan.md`, `docs/site-architecture.md`, and
`docs/live-talk-storyboard.md` for the planned design.

## Building

Requires [Quarto](https://quarto.org) (tested with 1.10.18). No other runtime
dependency — the plain markdown engine is used throughout; no R, Python, or
Jupyter code cells are executed at render time.

```bash
quarto render
```

Output goes to `_site/` (gitignored). Open `_site/index.html` or
`_site/slides/llms-to-agents.html` in a browser.

## Verifying

```bash
bash scripts/verify.sh
```

Runs, in order: a full render, an internal-link check, a source-claim
reconciliation check, a numerical check of the softmax fallback table, a
numerical check of the neuron/backprop worked example, a numerical check of
the transformer path-length worked example, and an offline-dependency check
on the rendered slide output. See `docs/build-log.md` for the most recent
run's results, including any check that requires a human with a real browser
(this environment has no headless browser installed, by design — see the
implementation plan, decision D5).

## Repository layout

```
_quarto.yml              website + deck project configuration
index.qmd                site home page
resources.qmd            sources used so far, annotated
learn/                    self-contained learning modules (three, so far)
slides/                   the Reveal.js deck (three slides, historical prototype)
_includes/                shared interactive markup, reused by deck and site
assets/                   CSS and JavaScript (vanilla, no build step)
sources/                  source map and machine-checkable claim ledger
scripts/                  verification scripts
docs/                     planning prompt, decisions, build log, reviews, and design docs
.claude/skills/           local project Skill for reader-first lesson editing
```

## Sources and claims

Every substantive factual claim in this slice carries a claim ID (e.g.
`[S-01]`) that resolves in `sources/claims.csv` and is described in prose in
`sources/source-map.md`. `scripts/check_sources.py` checks this
mechanically in both directions: no claim ID without a source, and no unused
source row.

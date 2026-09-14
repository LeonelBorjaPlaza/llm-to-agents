# From LLMs to Agents — course site

A Quarto website and Reveal.js deck supporting a 45-minute conceptual talk for
PhD economists: *From LLMs to agents: what the model is, how it is built, and
how it begins to act.*

This material is co-produced with Claude Code under human review. Claude Code
drafts and verifies; a human reviewer approves substantive choices, final
wording, and every commit.

## Status

**This is a vertical slice, not the finished course.** It exists to prove the
architecture — Quarto website + Reveal.js deck + a browser-based interactive,
all static and offline-capable — before the remaining five learning modules,
the full deck, and the full resource library are built.

Currently present:

- a minimal site shell (`index.qmd`, `resources.qmd`);
- one complete, standalone learning module (`learn/softmax-sampling.qmd`);
- three live slides covering logits/softmax, training/maximum likelihood, and
  sampling/temperature (`slides/llms-to-agents.qmd`);
- one interactive (a softmax-and-sampling laboratory) with a no-JavaScript
  fallback;
- a source map and claim ledger (`sources/`) covering only the sources used
  in this slice.

Not yet built: the other five learning modules, the glossary, the full deck,
the agent-loop interactive, and the full curated resource library. See
`docs/prompts/01-research-and-plan.md` and the approved implementation plan
for the complete design.

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
reconciliation check, a numerical check of the softmax fallback table against
the live equation, and an offline-dependency check on the rendered slide
output. See `docs/build-log.md` for the most recent run's results, including
any check that requires a human with a real browser (this environment has no
headless browser installed, by design — see the implementation plan, decision
D5).

## Repository layout

```
_quarto.yml              website + deck project configuration
index.qmd                site home page
resources.qmd            sources used in this slice, annotated
learn/                    self-contained learning modules (one, so far)
slides/                   the Reveal.js deck (three slides, so far)
_includes/                shared interactive markup, reused by deck and site
assets/                   CSS and JavaScript (vanilla, no build step)
sources/                  source map and machine-checkable claim ledger
scripts/                  verification scripts
docs/                     the planning prompt, decisions, and build log
```

## Sources and claims

Every substantive factual claim in this slice carries a claim ID (e.g.
`[S-01]`) that resolves in `sources/claims.csv` and is described in prose in
`sources/source-map.md`. `scripts/check_sources.py` checks this
mechanically in both directions: no claim ID without a source, and no unused
source row.

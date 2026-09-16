# Site architecture (planning document)

Full future site map. Built pages are marked **built**; everything else is
planned but not created in this batch — no placeholder pages exist for
any of them.

**Standing design rule:** no lesson presupposes another. Every module is
self-contained; if it needs a concept from another module, it links to
that module rather than assuming the reader has already read it. This is
an extension of the existing rule that no module may assume the talk —
extended here to mean no module may silently assume another module either.

## Modules

| Module | Status | Extends storyboard segments | Depends on (link, not presuppose) |
|---|---|---|---|
| `learn/softmax-sampling.qmd` | **Built** | 8, 9, 10 (partial), 13 | none |
| `learn/neural-networks.qmd` | **Built** | 3, 7 (partial), 11 | none |
| `learn/why-transformers.qmd` | **Built** | 6, 7 | `learn/neural-networks.qmd` (linked, not assumed) |
| `learn/tokens-context.qmd` | Planned | 4, 5, 12 | none |
| `learn/transformers-attention.qmd` | Planned — natural sequel to `why-transformers.qmd`; covers the queries/keys/values mechanics that lesson deliberately stops before | 7 (full derivation) | `learn/why-transformers.qmd` (linked) |
| `learn/training.qmd` | Planned, **rescoped**: since gradient descent and backpropagation basics now live in `learn/neural-networks.qmd`, this module focuses on corpus-scale maximum likelihood, the pretraining→post-training family (correction A, CC3), and the autoregressive generation loop — not re-deriving backpropagation | 10 (full), 12 (full), 14 | `learn/neural-networks.qmd` (linked) |
| `learn/posttraining.qmd` | Planned — may be folded into `learn/training.qmd` rather than kept separate; decide when built | 14, 15 | `learn/training.qmd` (linked) |
| `learn/agents.qmd` | Planned | 16–20 | none required; benefits from `learn/why-transformers.qmd`'s architecture vocabulary (linked) |
| `glossary.qmd` | **Built** (reference-layer batch, 2026-09-15) — alphabetical, 98 entries with stable `{#id}` anchors, each linking to the lesson that teaches it; checked by `scripts/check_glossary.py` | all | none |

## Navigation tiers (reference-layer batch, 2026-09-15)

The navbar exposes four tiers: **Start** (Home, The Short Story), **Learn** (the seven main-path lessons, numbered in order), **Deep dives** (the three optional technical pages), and **Reference** (Milestones, Glossary, Resources); the prototype deck is linked last as "Slides (prototype)". `index.qmd` mirrors the same tiers.

## Non-module pages

| Page | Status |
|---|---|
| `index.qmd` | **Built** |
| `resources.qmd` | **Built**, and **re-curated** in the reference-layer batch (2026-09-15): 19 entries in five categories, distinct from the evidence ledger in `sources/`; checked by `scripts/check_resources.py` |
| `milestones.qmd` | **Built** (reference-layer batch, 2026-09-15) — a selective 17-entry timeline with a static rail (`_includes/_milestone-rail.qmd`) reusable by the deck |
| `slides/llms-to-agents.qmd` | **Built**, historical prototype under the superseded design; not rebuilt to the new storyboard in this batch |
| A rebuilt full deck matching `docs/live-talk-storyboard.md` | Planned, not started |
| `docs/practical-guide-spec.md`'s guide itself | Planned — this batch delivers the spec only, not the guide |

## Resource-library seed (carried forward, unverified specifics not asserted)

- 3Blue1Brown's *Neural Networks* series — candidate for
  `learn/neural-networks.qmd`'s further reading; exact chapters/timestamps
  unverified (tracked as gap G2 in `sources/source-map.md`).
- Anthropic's context-engineering and Claude Code documentation — candidates
  for `learn/agents.qmd` and `docs/practical-guide-spec.md`.
- Vaswani et al. — already promoted from "resource candidate" to an
  evidentiary source (S10) in this batch; will also anchor
  `learn/transformers-attention.qmd`'s full derivation when built.

## Ordering rationale

The built modules follow the storyboard's own order where possible
(softmax/sampling first, since it was already built in Stage 1; neural
networks and why-transformers next, since the talk's architecture-
motivation segments (6–7) need both). Planned modules follow the
storyboard's segment order: tokens/context, then the full attention
derivation, then training/post-training, then agents, then the glossary
last, once every term it indexes actually exists on the site.

## Spine + Visual Pass (2026-09-15)

`short-story.qmd` was rebuilt as the definitive conceptual spine: it now
opens with the governing question (how a ChatGPT-like system is built,
what exists after training, and what happens to your text), shows the
whole lifecycle once, and walks it in thirteen sections (finished
object; the smallest piece of a network; assembling the corpus; text to
tokens to vectors; recurrent networks to the transformer, with attention
explained before the paper is named; pretraining and the base model;
post-training and assistant behavior; fluency and evidence;
reasoning-oriented models in training and at inference; what happens
when you type; parameters, context, and external state; tools and the
agent loop, taught through one concrete tool call; the mental model),
each ending in a "go deeper" pointer, about a twenty-minute read.
Thirteen reusable course figures live in `_includes/_fig-*.qmd`
(lifecycle, runnable model, tiny network, data pipeline, token to
vector, RNN versus transformer, attention intuition, training stages,
reasoning and inference-time computation, inference loop, three stores,
tool round trip, and a wrapper for the agent loop), each with a stable
`fig-*` wrapper id checked by `scripts/check_short_story_figures.py`,
and share a five-category semantic palette defined in `assets/css/site.scss` (data, model, training,
context, system) so the live deck can reuse them. Glossary previews are a
progressive enhancement inlined in `_includes/_glossary-preview.html`
(loaded on every page via `include-after-body`, so no asset path is
needed at any page depth or site sub-path); they read the
rendered glossary at runtime, so the glossary stays the single source of
truth. `learn/using-models-well.qmd` gained a one-minute summary
(`_includes/_one-minute-version.qmd`); `learn/how-created.qmd` gained a
compact corpus subsection in §1; the main-path lessons link the first
important occurrence of key terms to the glossary, with no wording
changes.


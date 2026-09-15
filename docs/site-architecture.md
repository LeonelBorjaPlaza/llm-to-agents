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
| `glossary.qmd` | Planned — the concept index tying model/transformer/attention/assistant/workflow/Skill/tool/agent together explicitly | all | none |

## Non-module pages

| Page | Status |
|---|---|
| `index.qmd` | **Built** |
| `resources.qmd` | **Built** — grows as each module adds sources |
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

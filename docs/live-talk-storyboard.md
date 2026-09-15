# Live talk storyboard (planning document — not yet built)

This is a design document for the not-yet-built full talk. It replaces the
21-slide, 45-minute route from the superseded big plan. **No slides exist
for this storyboard yet.** The three slides in `slides/llms-to-agents.qmd`,
and any other early-drafted slides, are **style experiments, not approved
content** — their technical content is not required to survive into the
final presentation (see `docs/decisions.md`).

**Governing design rule (see `CLAUDE.md`):** no required live equation, no
required live demonstration. Every equation and every interactive is
optional/skippable in the talk and lives in full on the corresponding
`learn/*.qmd` module. Vocabulary still stays recognizable live — every
required term is still named and defined — only the full derivation and
worked numbers move to the site.

## The core story (what the deck must carry)

The live deck should contain only the conceptual story required to follow
this chain — nothing more:

**training data → neural network → transformer → next-token prediction →
training → assistant → tools → agent**

Everything else — tokens, embeddings, logits, softmax, the
multinomial-logit bridge, sampling and temperature, and similar detail —
helps *explain* that chain but is not itself part of it, and belongs on
the website (per `CLAUDE.md`'s slide-design rules), not on a slide, unless
a specific point in the story genuinely cannot land without it.

## Slide-design rules (see `CLAUDE.md` for the full statement)

- One primary idea per slide; very little on-screen prose; no
  paragraph-sized text blocks.
- Explanation lives primarily in the speaker narrative, not on the slide.
- Prefer a diagram, a label, an example, or one short statement over
  prose.
- An equation appears only when it materially improves the conceptual
  explanation — never because a website section has a derivation.
- No slide exists merely because a technical detail has a corresponding
  website section.
- Slide titles carry the takeaway, not just the topic's name.
- Overflow is a design failure to fix by cutting content, never by
  shrinking the font. Conservative density budget: ~40 words of on-slide
  text (excluding the title), body text no smaller than roughly
  28px-equivalent at 1280×720, at most one diagram or short equation per
  slide.

## Status of the segment table below

The table below is **content planning, not slide-ready wording** — it
describes what each part of the talk needs to cover and where it sits in
the timeline, not what will appear on screen. Several of its 21 segments
(4–6, 8–10, 12–13 especially) are supporting detail for the core story
above, not separate required beats; when the deck is actually built, this
table must be re-screened against the core story and the density rules
above, and many of these segments will likely merge, shrink to a single
label, move into speaker narrative, or drop from the slide sequence
entirely while their content stays fully available on the corresponding
website module.

Target: **35–40 minutes**, with reserved buffer/Q&A slack (the old design
had none). `docs/milestone-timeline.md` aggregates the same segment list
below into section-level totals — it is not a separately estimated
summary.

## Segments

| # | Segment | Core content (corrected framing) | Visual treatment | Live math | Source | Website module | Min | Cum |
|---|---|---|---|---|---|---|---|---|
| 1 | Title | Frame the hour; the one question the talk answers | Title slide | — | — | `index` | 0.5 | 0.5 |
| 2 | The puzzle | A system trained only to predict the next token writes working code, and is also confidently wrong — both facts trace to the same training objective (CC1). Roadmap. | Roadmap diagram | — | S1 | `index` | 1.5 | 2.0 |
| 3 | What an LLM is, and what it ate | A trained, parameterized function; internet-scale text that is curated and filtered, not "the internet" | Box diagram + funnel | — | S1, S2 | `neural-networks` | 1.5 | 3.5 |
| 4 | Tokens | Subword units named; token IDs as arbitrary indices | Token-chip illustration | — | S1 | `tokens-context` (not yet built) | 1.0 | 4.5 |
| 5 | Embeddings | Token → learned vector, named; not a lookup table | 2-D projection sketch | — | S2 | `tokens-context` (not yet built) | 1.0 | 5.5 |
| 6 | Why attention: the problem | Recurrence's sequential dependency; why relating distant positions needed a better answer (per `learn/why-transformers.qmd` §1–§3) | Two-sentence contrast + toy sequence | — | S10, S2 | `why-transformers` | 2.5 | 8.0 |
| 7 | The transformer block | Named, not derived: attention moves information between positions; a feed-forward/MLP layer does per-position computation — two distinct mechanisms in one repeating block (S-19) | Block diagram | — | S2, S10 | `why-transformers`, `neural-networks` | 2.0 | 10.0 |
| 8 | Logits: raw scores | Pre-softmax scores, named "logits" second (PR8); distinguished from the statistics logit function if a question arises | Vector → bar-of-scores | — | S2 | `softmax-sampling` | 1.0 | 11.0 |
| 9 | Softmax and the multinomial-logit echo | Same probability *mapping* as multinomial/conditional logit (PR1); **equation optional/skippable** — shown only if time allows | Interactive shown or described, presenter's choice | Optional: Eq. 1 | S2 | `softmax-sampling` | 2.5 | 13.5 |
| 10 | Training as maximum likelihood | Training maximizes conditional likelihood (PR2); **equation optional/skippable** | Corpus → per-position likelihood | Optional: Eq. 2 | S1, S2 | `softmax-sampling` (training math extends to a future `training.qmd`) | 2.5 | 16.0 |
| 11 | What the parameters are, and are not | Parameters encode statistical regularities, not a queryable record (CC1's first half) | Compression metaphor | — | S1 | `neural-networks` | 1.5 | 17.5 |
| 12 | Generating an answer | Selected token appended to context; next step reuses cached representations (PR3) — never "re-runs the whole thing" | Loop diagram + token counter | — | S1, S2 | `tokens-context` (not yet built) | 1.5 | 19.0 |
| 13 | Sampling and temperature | Argmax vs. sampling (no required live demo); temperature's Boltzmann etymology if asked | Static figure; interactive available but not required | — | S2 | `softmax-sampling` | 1.5 | 20.5 |
| 14 | Pretraining → post-training | Post-training as a **family** of methods (CC3, corrected); never lists system instructions as one of them (correction A) | Two-stage timeline | — | S1 | `posttraining` (not yet built) | 1.5 | 22.0 |
| 15 | Why it's confidently wrong | CC1's full statement; CC2's "tokens to think" framed as shorthand, not literal thought | Failure-mode table | — | S1 | `posttraining` (not yet built) | 1.5 | 23.5 |
| 16 | The ladder: model → agent | Base model → assistant → augmented LLM → workflow → agent | Five-rung ladder | — | S5 | `agents` (not yet built) | 2.0 | 25.5 |
| 17 | What a tool call is | PR5's corrected framing: generated structured output, interpreted by surrounding software | Round trip diagram | — | S6, S5 | `agents` (not yet built) | 2.0 | 27.5 |
| 18 | Skills, instructions, and memory | System instructions/retrieved information/tool results are inference-time **context**, never post-training (correction A) | Three-level disclosure diagram | — | S8 | `agents` (not yet built) | 1.5 | 29.0 |
| 19 | One concrete loop | Short version of the full agent loop; permissions, stopping conditions | Zone diagram, short path | — | S9, S5 | `agents` (not yet built) | 2.0 | 31.0 |
| 20 | Why coding, and why that's not enough | PR6's corrected verification framing: a passing test is evidence, not proof | Verifiable-vs-unverifiable contrast | — | S5, S9 | `agents` (not yet built) | 1.0 | 32.0 |
| 21 | Closing mental model | One sentence; pointer to the website as the primary product | Single statement + site URL | — | — | `index` | 1.0 | 33.0 |
| — | **Buffer / Q&A** | Reserved slack — the old design had none | — | — | — | — | 3.0–4.0 | 36.0–37.0 |

**Total: 36.0–37.0 minutes**, inside the 35–40 target with genuine slack,
unlike the superseded 45-minute design's zero-slack, two-protected-equation
route.

Every segment's source citation is reused from the already-approved source
set (S1–S10); none of the timings, titles, or sources above are new
research — this document only re-sequences and re-times what the
implementation plan already established, adjusted for the corrected
technical framing (CC1–CC5, PR1–PR10) and the new no-required-math policy.

See `docs/milestone-timeline.md` for the section-level rollup of this same
segment list and the overrun/compression policy, and `docs/site-architecture.md`
for how each segment's website module fits into the full site map.

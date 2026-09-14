# CLAUDE.md — From LLMs to Agents course site

Concise project instructions for any Claude Code session working in this
repository. Binding for all stages, not just the vertical slice.

## What this is

A Quarto website + Reveal.js deck for a 45-minute conceptual talk aimed at
PhD economists in a research group at a multilateral development bank:
*From LLMs to agents: what the model is, how it is built, and how it begins
to act.*

**Product hierarchy.** The live presentation is a carefully selected
45-minute path through the material. The website is the fuller, standalone
learning resource — deeper explanations, mathematics, examples,
interactives, and curated references. Someone who never attended the talk
must be able to learn the material from the website alone. Slides link to
their corresponding website module; modules never assume the slides.

## Audience and pedagogical standard

PhD economists: strong in probability, maximum likelihood, optimization,
linear algebra, multinomial/conditional logit, and empirical research; mostly
**not** machine-learning researchers or software engineers. Do not water down
the mathematics. Do not assume architecture fluency. Every core concept
should move from problem → small example → the mathematical object →
plain-language intuition → real-model consequence → a link to deeper
website content.

## Source and safety rules

- Every substantive factual claim carries a claim ID (e.g. `[S-01]`) that
  resolves in `sources/claims.csv`, in both directions — no claim without a
  source row, no unused source row.
- Use original, authoritative sources (see `sources/source-map.md`). Do not
  reproduce third-party figures, animations, screenshots, or transcripts.
  Redraw all diagrams in inline SVG or Mermaid.
- Cite documentation pages with an **access date**, never a publication date
  (they display none). Cite arXiv formulas **by section**, not by equation
  number, where the paper leaves them unnumbered.
- Never invent a token ID, a timestamp, a duration, or a source detail. If a
  fact cannot be verified, mark it unverified or drop it — do not estimate.
- This repository may eventually be made public. Never place internal
  institutional documents, survey responses, account information, or private
  coordination material from outside `course-site/` into this repository.
  The parent coordination package is out of scope and stays private.

## Content accuracy corrections (binding — apply throughout)

These correct real overstatements caught at review. They are not stylistic
preferences.

**CC1 — Hallucination.** Do not state that lossy parameter storage or
sampling is "the hallucination mechanism." Use:

> The training objective rewards plausible continuation rather than
> independent verification of truth. The parameters encode statistical
> regularities rather than a directly queryable source record. Without
> grounding or external checks, a plausible continuation can therefore be
> unsupported or false.

Sampling affects variability but is not the root cause. Deterministic
decoding can also produce unsupported claims.

**CC2 — Intermediate reasoning.** Treat "models need tokens to think" as
informal shorthand, not a claim. Prefer:

> On some difficult tasks, generating intermediate reasoning tokens provides
> additional inference-time computation and can improve performance.

Do not equate generated reasoning with human thought.

**CC3 — Post-training.** Describe post-training broadly: supervised
instruction tuning; preference optimization or reinforcement learning;
safety and behavior shaping; product-level system instructions. RLHF may be
mentioned as one example, never as the universal or complete process.

**CC4 — Attention heads.** State that multiple heads allow several attention
patterns to operate in parallel. Do not imply that each head has a clean,
stable, human-interpretable function.

## Precision rules (binding — apply throughout)

**PR1 — Softmax and multinomial logit.** Describe next-token softmax as
using the same probability mapping as multinomial/conditional logit. Do not
say the entire language model is a multinomial-logit model. Live slide title:
"Softmax uses the multinomial-logit probability map."

**PR2 — Maximum likelihood.** Use:

> This is maximum-likelihood training, but it is not a conventional
> econometric exercise aimed at identifying interpretable structural
> parameters or reporting classical standard errors.

Do not imply that uncertainty measures are mathematically impossible.

**PR3 — Autoregressive generation.** Do not say the model "reruns the whole
thing" from scratch after every token. Use:

> The selected token is appended to the context, and the model performs the
> next prediction step, usually reusing cached representations from earlier
> tokens.

**PR4 — Tokenization.** Qualify tokenizer-specific claims: "In many commonly
used subword tokenizers, spaces and punctuation influence the split." And:
"Tokenization helps explain why spelling, character counting, and some
string operations can be awkward for LLMs." Do not present tokenization as
the sole cause of every spelling or counting failure.

**PR5 — Tool calls.** Do not use "the model only ever emits tokens — that is
the whole trick." Use:

> At the model boundary, a tool call is generated output in a structured
> format. The surrounding software interprets that output, executes the
> action, and returns the result to the next model call.

**PR6 — Verification.** Use:

> A passing test provides evidence that the specified checks passed. It does
> not establish that the specification, research design, or resulting
> number is correct.

Do not say a green test by itself proves correctness.

**PR7 — IIA and the multinomial-logit analogy.** Do not say "there is no
IIA." For fixed logits the algebraic odds-ratio property survives. Use:

> For fixed logits, softmax preserves the algebraic odds-ratio property
> associated with IIA. It should not be given a behavioral random-utility,
> structural, or welfare interpretation here because the logits are
> context-dependent neural-network outputs rather than estimated utility
> indices.

## Build commands

```bash
quarto render          # build the full site + deck to _site/
bash scripts/verify.sh # render + all verification scripts
```

No R, Python, or Jupyter code cells execute at render time (the plain
markdown engine is used throughout). Numerical examples are precomputed and
checked by `scripts/check_softmax_reference.py`, or computed live in the
browser by hand-written vanilla JavaScript with no build step and no network
dependency.

## No task is complete until

1. `quarto render` succeeds with no new warnings.
2. `bash scripts/verify.sh` passes, or every failing/skipped check is
   reported honestly (a human-browser check with no headless browser
   available is reported as skipped-pending-human, never as passed).
3. The diff has been shown and reviewed before any commit.
4. Nothing outside `course-site/` was read, written, or depended upon.
5. Nothing was installed, cloned, or pushed without explicit approval.

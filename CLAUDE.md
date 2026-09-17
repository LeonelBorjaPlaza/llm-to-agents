# CLAUDE.md — From LLMs to Agents course site

Concise project instructions for any Claude Code session working in this
repository. Binding for all stages, not just the vertical slice.

## What this is

A Quarto website + Reveal.js deck supporting a 30-minute conceptual talk
(about 28 minutes of prepared delivery plus a 2-minute reserve; retargeted
from 35–40 minutes on 2026-09-16, with optional technical depth kept on the
website) and a standalone learning resource for readers who are comfortable
following mathematical ideas but may not use them every day:
*From LLMs to agents: what the model is, how it is built, and how it begins
to act.*

**Product hierarchy.** The website is the primary, standalone learning
product — deeper explanations, mathematics, examples, interactives, and
curated references. Someone who never attended the talk must be able to
learn the material from the website alone. The live talk is a carefully
selected, lower-math path through it: it still names and defines every
required term even where the term's full treatment lives only on the
website — vocabulary stays recognizable live; depth, not recognition, moves
to the site. Slides link to their corresponding website module; modules
never assume the slides.

**Superseded design note.** An earlier design required two live-shown
equations (softmax; the maximum-likelihood training objective) and a full
live interactive demonstration in the talk, with an explicit "never cut"
rule protecting them, inside a 45-minute run time. That framing is
superseded: the talk carries **no required live equation and no required
live softmax demonstration**. Both are worked in full on the website; the
talk only needs to point to them. The three-slide Stage 1 deck that was
built under the old framing is left as a historical prototype — it is not
retrofitted to the new policy.

**Vocabulary hierarchy.** State this explicitly wherever the terms are
introduced: an LLM is the trained model; a transformer is a specific
neural-network architecture; inside each transformer block, self-attention
is one mechanism (it moves information between positions) and a
feed-forward/MLP layer is another (it does per-position nonlinear
computation) — two distinct components of the same repeating block, not
alternative names for the same thing. `[S-19]`

## Reader model (revised — no longer economist-specific)

**The course is written for a general reader with above-average
quantitative ability, not for a specialist and not for any named
profession.** Assume the reader:

- can follow an equation when its pieces are explained;
- understands basic probability and algebra;
- may have encountered calculus, optimization, or statistics before, but
  not necessarily recently;
- does not use mathematical notation every day;
- will **not** necessarily remember a symbol, definition, or mechanism
  introduced several pages earlier;
- has little or no machine-learning vocabulary.

Do not water down the mathematics. Do not name or assume any specific
profession, degree, or field as the audience, anywhere in reader-facing
text — not "economists," not "PhD," not "this audience already knows."
A discipline-specific analogy (e.g. the multinomial-logit bridge in
`learn/softmax-sampling.qmd`) may still appear, but framed as optional and
conditional ("for readers who already know X"), never as a description of
who the course is for.

**Assume intelligence, not prior vocabulary.** A reader does not need
every idea translated into an everyday metaphor. The reader needs
unfamiliar terms defined cleanly, a reason the concept matters, and enough
context to follow the next step. For a difficult concept the preferred
order is:

> problem or motivation → plain literal explanation → concrete example
> where useful → technical term → mathematics where it adds
> understanding → analogy only if something is still difficult

Do not mechanically include every element. Three further requirements:

**1. Give brief reminders, not silent reliance, when a concept returns.**
Do not assume notation or a definition "stays fresh" once introduced. When
an earlier concept becomes load-bearing again, restate it in one short
clause before using it — the shortest reminder that restores context, not
a mechanical repetition of the original definition. Never write "as you
know," "recall," or anything that assumes the reader remembers something
solely because it appeared earlier. For example, prefer:

> Earlier we called backpropagation the procedure that works backward
> through the network to calculate how a small change in each weight
> would change the loss. Those quantities are the gradients the optimizer
> now uses to change the weights.

Do not restate whole definitions merely because several sections have
passed; a clause is enough.

over the unexplained "Backpropagation gives us the gradients."

**2. Reduce jargon aggressively.** A technical term may appear only if
(a) it is needed, (b) it is explained at first meaningful use, and
(c) the explanation says what problem the term's concept solves or why it
is needed — not just what the term is called. Prefer the ordinary-language
description before the technical label:

> The model first produces one raw score for every possible next token.
> Machine-learning literature usually calls these scores logits.

not "The model produces logits." Do not introduce a technical term merely
because it is technically correct; if an idea can be explained accurately
without naming a term yet, do that first and name the term afterward. Do
not assume a glossary can compensate for unexplained prose — the main text
itself must remain understandable on its own.

**3. An analogy is optional.** Use one only when all four conditions
hold: (a) the literal explanation remains difficult to visualize; (b) the
analogy maps cleanly onto the mechanism; (c) it does not introduce
behavioral, causal, probabilistic, psychological, or physical implications
absent from the real mechanism; (d) the lesson will not later need to
unteach it. If the literal explanation is clearer than the analogy, omit
the analogy. A surviving analogy is written inline as a sentence or two,
not as a repeated "Think of it this way" box or any other structural
template. Avoid metaphors for their own sake, childish language,
unnecessary anthropomorphism, personality language applied to
mathematical objects, and replacing precise technical vocabulary with
vague everyday words after the technical term has been explained.

*Superseded at the 2026-09-15 audit: an earlier version of this rule
required a "Think of it this way" callout after every difficult concept.
That produced analogies that made mechanisms less precise (preference
readings of logits, a behavioral reading of softmax, a "kink" for a smooth
sigmoid, causal "contributed to the error" language for a gradient). The
callouts were removed from all three lessons.*

**Explanation standard.** The subject may be technically difficult; the
prose should not make it feel more difficult than it is. Aim for simple
language without loss of precision, concrete examples before
abstractions, short reminders when concepts
return, explanations that make the *reason* for each mechanism apparent,
and mathematical notation only after the reader understands what the
notation is describing. A reader should finish a difficult section
thinking "I understand why this exists and roughly how it works, even if
I could not reproduce the mathematics from memory." Do not confuse
sophistication with compression, and do not write down to the reader —
simplify the explanation, not the idea. If simplifying a sentence would
make it technically false, keep the necessary qualification and explain
it more clearly instead of dropping it.

Public lesson pages (`learn/*.qmd`) read as course content, not production
commentary. Do not narrate what a module "chose to include," what it
"deliberately does not build," or otherwise talk about the module's own
construction — that belongs in `docs/`, never in a reader-facing lesson.

## Slide-design rules (for the not-yet-built full deck)

**The Stage 1 slides, and any other early-drafted slides, are style
experiments, not approved content.** Their technical content is not
required to survive into the final presentation. The live deck should
carry only the conceptual story needed to follow: training data → neural
network → transformer → next-token prediction → training → assistant →
tools → agent. Technical detail that helps explain those ideas but is not
necessary to follow the story belongs on the website, not on a slide.

- One primary idea per slide.
- Very little prose on screen; no paragraph-sized blocks of text.
- Explanation belongs primarily in the speaker narrative, not on the
  slide — the slide is a visual anchor, not a transcript.
- Prefer a diagram, a label, a short example, or a single short statement
  over prose wherever one of those can carry the point instead.
- An equation appears only when it materially improves the conceptual
  explanation — not because the website has a corresponding derivation.
- No slide exists merely because a technical detail has a corresponding
  website section.
- Slide titles carry the takeaway, not just the topic's name (e.g. "The
  model never learned facts — it learned patterns," not "Parameters").
- Treat overflow as a design failure to fix by cutting or restructuring
  content, never by shrinking the font.
- **Conservative slide-density rule, for 1280×720 presentation viewing:**
  no more than about 40 words of on-slide text (excluding the title), body
  text no smaller than roughly a 28px-equivalent size, and no more than one
  diagram or one short equation per slide. If a point needs more than
  that to land, split it across two slides or move the remainder to
  speaker notes.

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

**CC3 — Post-training.** Describe post-training broadly, as a family of
methods, not one universal fixed sequence: supervised instruction tuning;
preference optimization or reinforcement learning; safety and behavior
shaping. RLHF may be mentioned as one example, never as the universal or
complete process.

*Corrected at this batch's review: an earlier version of this rule
incorrectly listed "product-level system instructions" as a post-training
method. It is not.* **Training and post-training change model parameters.**
System instructions, retrieved information, tool results, and other
supplied state change **inference-time context** — they never touch the
model's parameters and are never a form of post-training. Do not classify
system instructions as post-training anywhere in this repository.

**CC4 — Attention heads.** State that multiple heads allow several attention
patterns to operate in parallel. Do not imply that each head has a clean,
stable, human-interpretable function.

**CC5 — Backpropagation vs. the weight update.** Backpropagation computes
the gradient of the loss with respect to every parameter via the chain
rule, in one backward sweep. It does not, by itself, change any parameter.
A separate optimizer step (plain gradient descent, or a more sophisticated
rule such as Adam) uses that gradient to update the parameters. Do not
describe backpropagation as performing the update itself.

## Precision rules (binding — apply throughout)

**PR1 — Softmax and multinomial logit.** Describe next-token softmax as
using the same probability mapping as multinomial/conditional logit. Do not
say the entire language model is a multinomial-logit model. This is a
website-level bridge for readers who already know discrete-choice models
(see PR7) — it is not assumed to appear on any future live slide; per the
slide-design rules above, whether it earns a slide at all depends on
whether it is necessary to follow the live talk's core story.

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

The multinomial-logit connection is an optional mathematical bridge for
readers who already know discrete-choice models — present it that way
(clearly separable from the main teaching thread), not as required reading,
and without commentary about the reader or the course itself.

**PR8 — "Logit" has two meanings; do not conflate them.** In this course,
"logit" denotes the network's raw, pre-softmax real-valued score (see
PR1) — introduce that generic pre-softmax score first, and attach the term
"logit" to it second. This is **not** the same object as the statistics or
econometrics logit function, `logit(p) = log(p/(1-p))`, the log-odds
transform of an already-computed probability. Statistics' logit takes a
probability in [0,1] and returns a real number; the machine-learning usage
starts with an arbitrary real number (the score) and softmax turns it into
a probability. The exact relationship holds only for *differences* of
scores: under softmax with temperature `T`, `log(p_i/p_j) = (z_i - z_j)/T`,
and for exactly two candidates `logit(p_1) = (z_1 - z_2)/T`, which reduces
to `z_1 - z_2` only at `T = 1`. An individual multiclass score `z_i` is
not `logit(p_i)`. Do not write the unqualified `T = 1` form without saying
`T = 1`. *(Corrected at the 2026-09-15 audit: an earlier version said the
two "share a name and a family resemblance, not an object", which
understated the exact two-candidate relationship.)*

**PR9 — Prompting and model-use recommendations.** Qualify any prompting or
model-use recommendation by task, model, provider, and documentation date
where appropriate. Do not turn one vendor's guidance, or one model's
behavior, into a universal rule.

**PR10 — Historical claims.** Avoid unsupported historical "first" claims.
State what a specific, cited source says an architecture or technique does,
not that it was the first to do it, unless a source directly supports that
specific priority claim.

**On preserving earlier wording.** Do not preserve an inaccurate sentence
merely because it appeared in an earlier correction or precision rule above.
Preserve the underlying technical intent; document substantive corrections
where you make them (as CC3 does above).

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

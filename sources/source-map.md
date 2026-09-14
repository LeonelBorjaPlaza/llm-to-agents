# Source map — vertical slice

Human-readable companion to `sources/claims.csv`. Every claim ID used in
`learn/softmax-sampling.qmd` or `slides/llms-to-agents.qmd` appears here and
in the CSV; `scripts/check_sources.py` checks both directions
mechanically — no claim ID without a row, no row that no page cites.

This slice deliberately draws on only two of the eventual course's
evidentiary sources (Set A in the implementation plan), because it covers
only softmax, sampling, and temperature.

## Sources used in this slice

**S1 — Andrej Karpathy, *Deep Dive into LLMs like ChatGPT*.**
<https://www.youtube.com/watch?v=7xTGNNLPyMI>. Published 2025-02-05, 3h31m.
Principal narrative anchor for the whole course; here used for the
inference/sampling segment and the hallucination discussion.

**S2 — 3Blue1Brown, *Transformers, the tech behind LLMs*.**
<https://www.3blue1brown.com/lessons/gpt> (video:
<https://www.youtube.com/watch?v=wjZofJX0v4M>). Here used specifically for
the softmax-and-temperature segment at 22:22.

## Claim-by-claim

| ID | Claim (short) | Source | Locator | Support | Confidence | Caveat |
|---|---|---|---|---|---|---|
| S-01 | Softmax's constant-shift invariance | Mathematical identity | checked by `check_softmax_reference.py` | direct | high | Not a citation-dependent claim |
| S-02 | Softmax shares multinomial/conditional logit's mapping; the LLM is not a logit model | Mathematical identity / standard definition | functional-form comparison (PR1) | inference | high | Functional-form comparison only |
| S-03 | Algebraic odds-ratio (IIA) property survives for fixed logits; no behavioral reading | Mathematical identity | algebraic derivation (PR7) | inference | high | Explicitly not a structural claim |
| S-04 | Temperature rescaling; $T\to0$ / $T\to\infty$ limits | S2 | 22:22, "Softmax with temperature" | direct | high | Tie case for $T\to0$ is this site's own addition |
| S-05 | Softmax → categorical distribution; training = conditional-likelihood maximization / NLL minimization | S1 | ~20:11, "neural network internals" | direct | high | MLE framing is this course's restatement |
| S-06 | This MLE training is not conventional econometric identification; uncertainty measures not impossible | — (editorial) | Precision rule PR2 | inference | high | Correction adopted at external review |
| S-07 | Sampling varies output without changing parameters, inside a real generation loop | S1 | ~26:01, "inference" | direct | high | — |
| S-08 | Training rewards plausible continuation, not verified truth; deterministic decoding can also hallucinate | S1 (general) | ~1:20:32, "hallucinations, tool use, knowledge/memory" | inference | medium-high | **Own synthesis (correction CC1). Timestamp not independently re-verified in this slice — see "Open verification debt" below.** |

## Open verification debt (carried forward from the implementation plan)

- **G1.** None of the Karpathy timestamps above (S-05, S-07, S-08) have
  been independently re-verified against the live video by this session —
  they were produced by an earlier read-only reconnaissance pass and are
  "good enough to plan against but not yet good enough to publish," per
  the approved plan. **Before any Stage 2 publication, re-verify all three
  against the live video.**
- The 3Blue1Brown timestamp (S-04) is similarly unverified in this session.
- S-02, S-03, and S-06 are marked `inference` because they are this
  course's own editorial framing (per precision rules PR1, PR7, and
  correction/rule PR2), not a direct claim made by either video. This is
  intentional and should not be "fixed" by attributing them to S1 or S2.

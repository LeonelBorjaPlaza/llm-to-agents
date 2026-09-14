# Stage 1 first-learner review

This is a prototype checkpoint, not publication approval. Nothing built in
Stage 1 has been approved for the audience. It exists to test the
architecture before more content is built on top of it. The decisions this
review produced are recorded separately, in docs/decisions.md.

## What worked

- The one-module, three-slide shape proved the architecture end to end: a
  Quarto website and a Reveal.js deck share one interactive component,
  included from a single source file, with a working no-JavaScript
  fallback.
- Ordinary website pages render small and fast (24-48 KB) once
  embed-resources and self-contained-math were scoped to the deck alone
  instead of applied to every page.
- The multinomial-logit bridge in learn/softmax-sampling.qmd is a useful
  hook for this audience. It states plainly where the analogy holds (the
  algebraic odds-ratio property) and where it does not (no behavioral or
  welfare interpretation).
- The numerical fixture is checked by a script, not just proofread by eye.
  A digit error in the fallback table would be caught before it shipped.
- The claim-ID system worked as intended. Every substantive claim in the
  prototype traces to a source or is explicitly marked as this course's
  own editorial framing.

## What did not work

- The offline-math check failed, for a specific and well-understood
  reason, not a typo. Quarto's embed-resources and self-contained-math
  options do not stop the Reveal.js math plugin from building a script
  tag at runtime that fetches KaTeX or MathJax from cdn.jsdelivr.net. This
  was confirmed directly in the rendered deck, where that hostname appears
  four times inside inlined script blocks. The automated check correctly
  reports this as a failure, and it remains unresolved. This batch does
  not vendor KaTeX and does not build an equation-image workaround; that
  decision is still open.
- Every browser-dependent check is still pending. No headless browser is
  installed in this environment. Opening the site, opening the deck,
  exercising the interactive, exercising its no-JavaScript fallback,
  opening the deck with the network disabled, and confirming speaker notes
  and navigation all require a human with a real browser, and none of them
  have been performed yet.
- A 45-minute talk with two required live equations and a full live
  interactive demonstration left no slack. Building three slides already
  used most of the available margin before any of the agent material
  existed.
- Some of the reader-facing prose read as internal notes rather than
  course content, for example a sentence describing what "this module"
  chose to include. A standalone lesson should teach the reader something,
  not narrate its own construction.
- Two technical errors surfaced independently and are corrected in this
  batch: the existing post-training rule in CLAUDE.md incorrectly listed
  system instructions as a post-training method, when system instructions
  are inference-time context and do not change model parameters; and
  nothing in Stage 1 yet distinguished the machine-learning sense of
  "logit" (a raw, pre-softmax score) from the statistics sense (the
  log-odds transform of a probability), which is a real risk for an
  audience already fluent in logit models.

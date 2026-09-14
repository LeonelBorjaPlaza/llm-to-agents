# Decisions

Public-safe decision log for this repository. Limited to information safe
to retain in a potentially publishable repository — no internal
institutional documents, survey responses, account information, or private
coordination material.

| Date | Decision | Reason | Alternatives rejected | Decided by |
|---|---|---|---|---|
| 2026-09-14 | Adopt the `course-site` file tree (this run's specification) rather than an earlier, broader scaffold draft. | The earlier draft predates and conflicts with the approved plan's narrower scope for this stage. | Reconciling both trees; deferred until Stage 2. | External review |
| 2026-09-14 | Approve Stage 0 (Git init) and Stage 1 (vertical slice) only. Stage 2 (full deck, remaining modules, full resource library) is not approved. | Prove the architecture — Quarto website, Reveal.js deck, one interactive, all offline-capable — before committing to the full build. | Building the full course before any external review. | External review |
| 2026-09-14 | Test Quarto's native `embed-resources` + `self-contained-math` for offline math rendering before considering any vendored library. | Empirical test, not an assumption; avoids an unnecessary dependency if the native option works. | Vendoring KaTeX immediately; hand-authored equation SVGs. | External review |
| 2026-09-14 | No tokenization component in this slice; no `tiktoken` installation. When built, use illustrative subword splits with no token IDs — token IDs are arbitrary and not pedagogically necessary. | Avoids an unneeded install and avoids implying any specific tokenizer is Claude's. | Installing `tiktoken`; capturing IDs from a third-party tool. | External review |
| 2026-09-14 | No browser-automation tooling (Playwright, Chromium, Node, or any new plugin/Skill) in this slice. Use a documented human browser checklist instead. | Keeps the vertical slice dependency-free; automation is reconsidered only after this slice is reviewed. | Installing Playwright + Chromium now. | External review |
| 2026-09-14 | Six content-accuracy corrections (hallucination mechanism, "tokens to think," post-training scope, attention-head interpretability, autoregressive caching, tool-call framing) and the multinomial-logit/MLE precision rules are binding from this stage forward and recorded in `CLAUDE.md`. | Several draft claims overstated or misstated real mechanisms; corrected at external review before any content shipped. | Leaving the original phrasing and correcting later. | External review |

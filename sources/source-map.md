# Source map — vertical slice

Human-readable companion to `sources/claims.csv`. Every claim ID used in
`learn/softmax-sampling.qmd` or `slides/llms-to-agents.qmd` appears here and
in the CSV; `scripts/check_sources.py` checks both directions
mechanically — no claim ID without a row, no row that no page cites.

This batch adds two new lessons (neural networks; why transformers) on top
of the Stage 1 softmax module, and reuses the same evidentiary source set
plus one new source. The 2026-09-15 cold audit added three further primary
sources (S11–S13 below), each verified at the abstract only, for the
"why transformers became prevalent" section.

## Sources used

**S1 — Andrej Karpathy, *Deep Dive into LLMs like ChatGPT*.**
<https://www.youtube.com/watch?v=7xTGNNLPyMI>. Published 2025-02-05, 3h31m.
Principal narrative anchor for the whole course; here used for the
inference/sampling segment and the hallucination discussion.

**S2 — 3Blue1Brown, *Transformers, the tech behind LLMs*.**
<https://www.3blue1brown.com/lessons/gpt> (video:
<https://www.youtube.com/watch?v=wjZofJX0v4M>). Used for the
softmax-and-temperature segment at 22:22, the "premise of deep learning"
segment at 7:20, and the "inside a transformer" segment at 3:03.

**S10 — Vaswani et al., *Attention Is All You Need*.**
<https://arxiv.org/abs/1706.03762> (v7, 2023-08-02). New to this batch.
Used for Section 1's discussion of recurrence's sequential dependency,
Section 3.1's encoder/decoder sub-layer structure, and Section 4's Table 1
(complexity, sequential operations, and maximum path length by layer
type). **Verified directly against the live paper (PDF) on 2026-09-14** —
see the exact figures below; this is not a reused, unverified timestamp
like the S1/S2 rows. On 2026-09-14 the abstract, Section 1 ¶1, Section
3.2.1, Section 3.2.3, and Section 4's "shorter these paths" sentence were
additionally verified verbatim against the arXiv HTML rendering (v7).

**S11 — Devlin et al., *BERT: Pre-training of Deep Bidirectional
Transformers for Language Understanding*.**
<https://arxiv.org/abs/1810.04805> (v2, 2019-05-24). New at the
2026-09-15 audit. Used only for the pretraining-and-transfer layer of
`learn/why-transformers.qmd` §5. **Abstract verified verbatim on
2026-09-15**; no other section of the paper was read or relied on.

**S12 — Kaplan et al., *Scaling Laws for Neural Language Models*.**
<https://arxiv.org/abs/2001.08361> (v1, 2020-01-23). New at the
2026-09-15 audit. Used only for the scaling layer of
`learn/why-transformers.qmd` §5. **Abstract verified verbatim on
2026-09-15**; no other section read.

**S13 — Brown et al., *Language Models are Few-Shot Learners*.**
<https://arxiv.org/abs/2005.14165> (v4, 2020-07-22). New at the
2026-09-15 audit. Used only for the in-context-behavior layer of
`learn/why-transformers.qmd` §5. **Abstract verified verbatim on
2026-09-15**; no other section read.

**S14 — Sennrich, Haddow, and Birch, *Neural Machine Translation of Rare
Words with Subword Units*.** <https://arxiv.org/abs/1508.07909> (v5,
2016-06-10). New in the tokens/context batch (2026-09-15). Used for the
subword-unit motivation and the BPE procedure in
`learn/tokens-context.qmd` §2. **Abstract verified verbatim on
2026-09-15.**

**S15 — Radford, Wu, Child, Luan, Amodei, and Sutskever, *Language Models
are Unsupervised Multitask Learners* (GPT-2).**
<https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf>
(OpenAI, 2019). New in the tokens/context batch. Used for byte-level BPE,
the space and punctuation merge rules, the 50,257-entry vocabulary, and
the 1,024-token context size. **Section 2.2 and the vocabulary/context
sentence in Section 2.3 verified against the PDF text (pdftotext) on
2026-09-15.**

**S16 — Bengio, Ducharme, Vincent, and Jauvin, *A Neural Probabilistic
Language Model*.** Journal of Machine Learning Research 3 (2003),
1137–1155. <https://www.jmlr.org/papers/volume3/bengio03a/bengio03a.pdf>.
New in the tokens/context batch. Used for the learned embedding table
(C as a |V| × m matrix of free parameters) and for why similarity
structure emerges. **Abstract, Section 1.1, and Section 2 verified
against the PDF text on 2026-09-15.**

**S17 — Anthropic, *Context windows* (Claude API documentation).**
<https://platform.claude.com/docs/en/build-with-claude/context-windows>,
**accessed 2026-09-15** (the docs.anthropic.com URL redirects here).
Product-specific; used, labeled as such, for the definition of a context
window, what counts toward it, and the up-to-1M-token size figure.

**S18 — Liu et al., *Lost in the Middle: How Language Models Use Long
Contexts*.** <https://arxiv.org/abs/2307.03172> (v3, 2023-11-20). New in
the tokens/context batch. Used for the placement effect in
`learn/tokens-context.qmd` §10. **Abstract verified verbatim on
2026-09-15.**

**S19 — Lewis et al., *Retrieval-Augmented Generation for
Knowledge-Intensive NLP Tasks*.** <https://arxiv.org/abs/2005.11401>
(v4, 2021-04-12). New in the tokens/context batch. Used only for the
general idea of retrieval placing external text into the context.
**Abstract verified verbatim on 2026-09-15.**

**S20 — Anthropic, *Effective context engineering for AI agents*
(engineering blog, published 2025-09-29).**
<https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>,
**accessed 2026-09-15**. Vendor guidance (PR9), used alongside S18 for
the practical-consequences section, attributed as one provider's
statement.

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
| S-09 | ML "logit" (pre-softmax score) vs. statistics "logit" (log-odds transform); $\log(p_i/p_j)=(z_i-z_j)/T$; two candidates: $\operatorname{logit}(p_1)=(z_1-z_2)/T$ | Mathematical definition + algebraic identity | definitional comparison (PR8) | direct | high | Corrected 2026-09-15 to state the exact $T$-qualified relationship |
| S-10 | Softmax named by contrast with hard argmax; returns a distribution, not the maximum value; approaches argmax as $T\to0$ | Mathematical identity / standard terminology | naming convention | inference | high | Corrected 2026-09-15: "argmax", not "max/argmax" |
| S-11 | "Temperature" borrowed from the Boltzmann distribution ($p_i\propto\exp(-E_i/kT)$) | Standard statistical mechanics | general physics identity | inference | high | Not attributed to S1/S2 without verification |
| S-12 | Neuron/layer definition; deep learning's general premise | S2 | ~7:20, "the premise of deep learning" | direct | high | Reused timestamp, open gap G1 |
| S-13 | Toy unit ≡ binary logistic regression; sigmoid+cross-entropy gradient simplification | Mathematical identity | checked by `check_neuron_example.py` | direct | high | — |
| S-14 | Backprop computes gradients only; a separate optimizer step updates parameters | Mathematical identity / standard definition | correction CC5 | inference | high | Checked by `check_neuron_example.py` |
| S-15 | Affine layers without nonlinearity compose to one affine map | Mathematical identity | linear algebra | direct | high | Reworded 2026-09-15: "affine", since layers carry biases |
| S-16 | Recurrent layer: $O(n\cdot d^2)$ complexity, $O(n)$ sequential ops, $O(n)$ max path length; sequential dependency blocks intra-example parallelization | S10 | §1 ¶2; §4/Table 1, Recurrent row | direct | high | **Verified against the live paper 2026-09-14.** $n{=}8$ figures are this course's own instantiation, checked by `check_transformer_path_lengths.py` |
| S-17 | Self-attention layer: $O(n^2\cdot d)$ complexity, $O(1)$ sequential ops, $O(1)$ max path length; shorter paths make long-range dependencies easier to learn | S10 | §4/Table 1, Self-Attention row; §4 "shorter these paths" sentence | direct | high | **Verified against the live paper 2026-09-14.** No implementation-memory claim; FlashAttention out of scope this batch |
| S-18 | Quadratic attention cost has motivated alternative approaches (sparse/local/linear attention, state-space models) | General field characterization | editorial synthesis | inference | medium | Deliberately generic; no "first" claim, no specific technique endorsed |
| S-19 | Hierarchy: LLM ⊃ transformer (architecture) ⊃ block ⊃ {self-attention, feed-forward/MLP} as two distinct mechanisms | S2; S10 | S2 ~3:03; S10 §3.1 | direct | high | **S10 locator verified 2026-09-14.** S2 timestamp reused, open gap G1 |
| S-20 | Transformer prevalence emerged from the combination of architectural advantages and subsequent empirical success, not one property or paper | Editorial synthesis of S-16/17/21/23–26 | — | inference | medium | Rewritten 2026-09-15; earlier "investment flywheel" framing dropped as too causal |
| S-21 | Dominant pre-2017 models recurrent or convolutional; LSTM/GRU established; Transformer superior in quality, more parallelizable, less training time on its two translation tasks | S10 | Abstract; §1 ¶1 | direct | high | **Verified verbatim 2026-09-14 (arXiv HTML v7)** |
| S-22 | Decoder self-attention masked so a position cannot attend to subsequent positions | S10 | §3.2.3 | direct | high | **Verified 2026-09-14.** Stated in the paper's "subsequent positions" terms; no indexing-convention claim |
| S-23 | Dot-product attention implemented with highly optimized matrix multiplication; architecture allows significantly more parallelization | S10 | §3.2.1; §1 final ¶ | direct | high | **Verified verbatim 2026-09-14.** Replaces an unsourced "GPUs built specifically" statement |
| S-24 | Pretrained BERT fine-tuned with one additional output layer for a wide range of tasks | S11 | Abstract | direct | high | **Verified verbatim 2026-09-15.** Encoder model; used only for the transfer layer of §5 |
| S-25 | Loss scales as a power law in model size, data, and compute over more than seven orders of magnitude | S12 | Abstract | direct | high | **Verified verbatim 2026-09-15.** Empirical regularity over the studied range, not a law |
| S-26 | GPT-3 (175B, autoregressive) applied without gradient updates; scaling improves task-agnostic few-shot performance | S13 | Abstract | direct | high | **Verified verbatim 2026-09-15.** CC2 applies: observed task performance, not thinking |
| S-27 | Subword units for open-vocabulary translation; BPE adapted to segmentation | S14 | Abstract; §3.2 | direct | high | **Verified 2026-09-15.** Toy merge example is the course's own, checked by `check_bpe_example.py` |
| S-28 | Byte-level BPE (256-byte base); "dog. dog! dog?" merge problem; no merges across character categories except spaces; 32k–64k BPE vocabularies common; GPT-2 vocabulary 50,257 and context 1,024 | S15 | §2.2; §2.3 | direct | high | **Verified against PDF text 2026-09-15.** One 2019 tokenizer; other families differ (PR4) |
| S-29 | Learned word feature vectors, jointly with the probability function; C is a \|V\| × m matrix of free parameters; similar words get similar vectors; m = 30–100 in experiments | S16 | Abstract; §1.1; §2 | direct | high | **Verified against PDF text 2026-09-15.** No "first" claim |
| S-30 | Learned embeddings to d_model-dimensional vectors; learned linear + softmax to next-token probabilities; shared matrix; position information must be injected | S10 | §3.4; §3.5 first sentence | direct | high | **Verified verbatim 2026-09-15 (arXiv HTML v7)** |
| S-31 | Context window = all text the model can reference incl. its response; everything in a request counts; turns accumulate; "context rot"; up to 1M tokens depending on model | S17 | "How the context window works"; "Context window sizes by model" | direct | high | **Product-specific, accessed 2026-09-15 (PR9).** Size figure will change |
| S-32 | Performance highest with relevant information at the beginning or end of a long context; degrades in the middle | S18 | Abstract | direct | high | **Verified 2026-09-15.** 2023 models and tasks; phrased as one study's finding |
| S-33 | Parametric knowledge access is limited; RAG combines parametric and non-parametric (retrieved) memory | S19 | Abstract | direct | high | **Verified 2026-09-15.** Used only for the general mechanism |
| S-34 | Context = tokens included when sampling; recall decreases as tokens grow; finite resource; smallest set of high-signal tokens | S20 | Opening sections | direct | medium-high | **Vendor guidance, accessed 2026-09-15 (PR9)**; paired with S-32 |
| S-35 | Tokenization helps explain awkwardness with spelling, character counting, and string operations; not the sole cause | — (course inference; PR4) | inference from S-27/S-28 | inference | medium | Course synthesis; no model-specific behavior asserted |

## Open verification debt (carried forward from the implementation plan)

- **G1.** None of the S1/S2 timestamps (S-05, S-07, S-08, S-12, S-19's S2
  locator) have been independently re-verified against the live video by
  this session — they were produced by an earlier read-only
  reconnaissance pass and are "good enough to plan against but not yet
  good enough to publish," per the approved plan. **Before any Stage 2
  publication, re-verify all of them against the live video.**
- The 3Blue1Brown timestamp (S-04) is similarly unverified in this session.
- **Resolved, not open:** the two new S10 locators (S-16, S-17) and S-19's
  S10 locator were independently verified directly against the live paper
  (PDF fetch) on 2026-09-14, unlike the reused S1/S2 timestamps above —
  this is the one bounded new-source check this batch performed, per the
  approved plan's "or unresolved gaps" clause.
- **G2 (new).** `learn/neural-networks.qmd`'s "continue learning" section
  names 3Blue1Brown's *Neural networks* series as a further resource
  **without** asserting a specific chapter number, timestamp, or URL —
  those specifics are unverified and must not be added until confirmed.
- **Resolved, not open (2026-09-15 audit):** S-21, S-22, S-23 (Vaswani
  abstract, §1, §3.2.1, §3.2.3, §4 sentence) and S-24, S-25, S-26 (the
  BERT, scaling-laws, and GPT-3 abstracts) were verified verbatim against
  the live arXiv pages in a bounded, abstract-only pass authorized for the
  "why prevalent" section. No other sections of those three papers were
  read; do not cite them for anything beyond the quoted sentences without
  a fresh verification.
- **Resolved, not open (tokens/context batch, 2026-09-15):** S-27–S-34
  were verified against the live sources on 2026-09-15 (arXiv abstract
  pages for S-27, S-32, S-33; the GPT-2 and Bengio PDFs via text
  extraction for S-28, S-29; arXiv HTML for S-30; the two Anthropic pages
  for S-31, S-34, which are product-specific and access-dated). The
  Karpathy tokenization segment cited as a learning resource on
  `learn/how-created.qmd` carries **no timestamp**, deliberately: none
  has been verified (same class of gap as G1).
- S-02, S-03, S-06, S-10, S-11, S-18, S-20, and S-35 are marked `inference`
  because they are this course's own editorial framing, naming convention,
  or field characterization — not a direct claim made by a video or paper.
  This is intentional and should not be "fixed" by attributing them to a
  source that doesn't actually state them.

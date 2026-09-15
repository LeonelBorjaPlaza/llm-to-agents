# Milestone timeline (planning document — not yet built)

Section-level timing, **recalculated directly from the full storyboard**
in `docs/live-talk-storyboard.md` — every number below is that document's
own per-segment minutes, summed by section, not a separately estimated
figure. If the storyboard changes, this document's totals must be
re-summed from it, not adjusted independently.

## Section totals

| Section | Storyboard segments | Minutes |
|---|---|---|
| Opening | 1–2 | 2.0 |
| Foundations: data, tokens, embeddings | 3–5 | 3.5 |
| Architecture motivation: why attention, the transformer block | 6–7 | 4.5 |
| The two mathematical bridges, parameters, generation, sampling | 8–13 | 10.5 |
| Post-training and failure modes | 14–15 | 3.0 |
| The agent bridge | 16–20 | 8.5 |
| Closing | 21 | 1.0 |
| **Subtotal** | 1–21 | **33.0** |
| Buffer / Q&A | — | 3.0–4.0 |
| **Total** | | **36.0–37.0** |

Inside the 35–40 minute target, with 3.0–4.0 minutes of genuine reserved
slack — a structural change from the superseded 45-minute design, which
had no slack once its two protected equation slides and full live
interactive demo were built.

## Overrun policy (re-derived for the new design)

The old design's policy protected two "never cut" live-equation slides,
because they were required. **No slide is required to carry a live
equation or a live demonstration in the new design** — every equation and
interactive is optional/skippable, worked in full on the corresponding
website module instead. This changes what compression means: instead of
protecting specific slides, the policy protects specific **narrative
beats**.

If running long, compress in this order:

1. **Cut buffer/Q&A first** (3.0–4.0 min available).
2. **Soften the two mathematical-bridge segments (9, 10) from "shown" to
   "named only"** — state the softmax and maximum-likelihood connections
   in one sentence each, without displaying the equations live. This was
   not available under the old design, where these equations were
   protected; it is the single largest lever in the new design.
3. **Trim post-training and failure-modes (segments 14–15) to
   headlines.**
4. **Shrink the agent-loop segment (19) to one diagram**, dropping the
   step-through.

**Never drop:** the puzzle/hook (segment 2), the "why attention" segment
(6), the ladder (segment 16), or the closing (segment 21) — these four
narrative beats replace the old design's two protected equation slides as
what must survive any compression.

## What changed from the superseded design

- 45 minutes → 35–40 minutes.
- Zero slack → 3.0–4.0 minutes of reserved buffer.
- Two required, "never cut" live equations → zero required live
  equations; both optional and both fully available on the website.
- A full live interactive demonstration required → no live demonstration
  required; the interactive lives in full on `learn/softmax-sampling.qmd`.
- Compression protected specific slides → compression protects specific
  narrative beats, since no slide is privileged by a required-equation
  status anymore.

See `docs/live-talk-storyboard.md` for the full segment-by-segment detail
these totals are summed from, and `docs/decisions.md` for the review that
produced this redesign.

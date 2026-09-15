---
name: reader-first-course-editor
description: Use when polishing prose in this repository's learn/*.qmd lesson pages — improving connected prose, transitions, examples, terminology, jargon load, and reader accessibility while preserving equations, citations, and claim IDs. Must flag (not silently apply) any edit that changes technical meaning, including in previously "approved" wording, and verify it against sources/claims.csv, CLAUDE.md's corrections, or general technical correctness before applying it. Not for slides/*.qmd, docs/*.md, or non-course prose.
---

# Reader-first course editor

A prose-quality editing pass for this repository's standalone lessons
(`learn/*.qmd`). Applied **after** first-draft technical writing is
complete, as a separate pass — not interleaved with drafting.

## What this Skill is for

Improving how a lesson *reads*: connected prose, natural transitions
between sections, sharper examples, consistent terminology, reduced
jargon load, and clear literal explanation where a concept needs it. It
is not for changing what technical claims a lesson makes, or restructuring
its section order — a jargon-reduction rewrite or a contextual reminder is
explanatory scaffolding around an existing claim, not a new one, and stays
in scope as long as it does not assert anything the lesson did not already
assert.

The governing principle: **assume intelligence, not prior vocabulary.** A
reader does not need every idea translated into an everyday metaphor. The
reader needs unfamiliar terms defined cleanly, a reason the concept
matters, and enough context to follow the next step. The standard is
simple without being simplistic, technically precise without being
compressed.

## Reader model (binding — read `CLAUDE.md`'s "Reader model" section in
full before editing; this is a summary, not a replacement for it)

- Write for a quantitatively capable general reader, not a specialist —
  no named profession, degree, or field as the assumed audience.
- Do not assume mathematical notation remains fresh after it was
  introduced.
- When an earlier concept becomes important again, give a brief
  contextual reminder — the shortest one that restores context, not a
  mechanical repetition of the original definition.
- Ordinary language comes before specialist terminology whenever
  possible.
- Define technical terms at their first meaningful use.
- Explain *why* a concept is being introduced — what problem it solves —
  not merely what it is called.
- **An analogy is optional.** Use one only when all four conditions
  hold: (1) the literal explanation remains difficult to visualize;
  (2) the analogy maps cleanly onto the mechanism; (3) it introduces no
  behavioral, causal, probabilistic, psychological, or physical
  implication absent from the real mechanism; (4) the lesson will not
  later need to unteach it. If the literal explanation is clearer than
  the analogy, omit the analogy (see the procedure step below).
- Remove jargon that does not pay for itself, but do not replace precise
  technical vocabulary with vague everyday words once the term has been
  explained.
- Prefer one concrete example before a general abstraction.
- A mathematically correct sentence that a non-specialist cannot parse is
  not finished.
- Read each section as though the reader arrived with no machine-learning
  vocabulary.
- Perform a second pass specifically looking for concepts whose
  definitions appeared too long ago for the current sentence to rely on
  them without a reminder.

## Procedure

1. **Read first, in full, before editing anything:** the target
   `learn/*.qmd` file, `sources/claims.csv`, `sources/source-map.md`, and
   `CLAUDE.md`'s content-accuracy corrections and precision rules. You
   cannot judge whether an edit changes technical meaning without knowing
   what the page currently claims and why.

2. **Classify every edit before making it**, as one of:
   - **PROSE** — wording, transitions, examples, or terminology change
     that leaves the technical content unchanged;
   - **MEANING** — a change to what the page actually asserts.

3. **For every MEANING edit**, before applying it:
   - write the *before* claim and the *after* claim, each in one
     sentence;
   - check the after-claim against the relevant `sources/claims.csv` row,
     a `CLAUDE.md` correction or precision rule, or direct independent
     verification (recompute a small worked example; check a definitional
     fact against a reliable standard source);
   - list it under a **"Flagged technical changes"** section in your
     output, with the before/after and how you verified it — never apply
     it silently just because the surrounding prose needed to change too.

4. **Never delete or renumber a claim ID.** If a sentence carrying an
   `[S-nn]` tag needs a meaning change, and the new wording is no longer
   supported by that row's source, **stop and ask** rather than inventing
   a new claim ID or quietly detaching the citation.

5. **Preserve equations verbatim** unless a genuine error is found in one.
   Any equation change is automatically a MEANING edit under rule 3, no
   matter how small it looks.

6. **Improve prose** freely within PROSE bounds: strengthen a transition
   between two sections, sharpen a worked example that already exists,
   tighten terminology toward the lesson's established house style
   (problem → example → object → intuition → consequence →
   misconceptions → check → resources), and vary sentence length and
   structure so the page does not read as a string of uniform declarative
   sentences. Do not add a new factual claim that would need its own
   citation — if the prose genuinely needs one, flag it as a required
   follow-up rather than adding it unasked.

7. **Audit and reduce jargon.** Read the section as though the reader has
   no machine-learning vocabulary. For every technical term: confirm it
   is needed, confirm it is explained at first meaningful use, and
   confirm the explanation says what problem the term's concept solves
   or why it matters — not just its name. Where a term appears before an
   ordinary-language description of the same idea, reorder so the
   ordinary-language description comes first and the term is attached
   second. List every term removed and every term (re-)explained.

8. **Audit every analogy against the four-condition gate.** For a
   difficult concept, the preferred order is: problem or motivation →
   plain literal explanation → concrete example where useful → technical
   term → mathematics where it adds understanding → analogy only if
   something is still difficult. Do not mechanically include every
   element. For each analogy already present, or one you are tempted to
   add, check all four conditions from the reader model above; delete or
   decline it if any condition fails. Reject an analogy if an important
   part of it does not correspond to the actual mechanism, or if the
   lesson later has to unteach it. A surviving analogy is written inline
   as one or two plain sentences, not as a templated callout box. Avoid
   metaphors for their own sake, childish language, unnecessary
   anthropomorphism, and personality language applied to mathematical
   objects (a temperature parameter is not "adventurous"; a score is not
   a "preference"). Never mention teaching level, audience, or these
   authoring instructions in reader-facing text.

9. **Second pass: aging definitions.** Re-read the file start to finish
   looking specifically for sentences that rely on a term, symbol, or
   mechanism defined many paragraphs or sections earlier, with no
   reminder. Add the shortest reminder that restores context — a clause,
   not a restated definition. Do not restate whole definitions merely
   because several sections have passed. Do not add "as you know,"
   "recall," or similar language anywhere.

10. **Remove leftover production or planning narration** from
   reader-facing text — sentences that describe what "this module" chose
   to include, or what it "deliberately does not build," rather than
   teaching the reader something. List what was removed, so nothing
   substantive is silently dropped along with it.

11. **Run checks after editing:**
   - `python3 scripts/check_sources.py`, always;
   - `python3 scripts/check_softmax_reference.py`, if the edited file is
     `learn/softmax-sampling.qmd`;
   - `python3 scripts/check_neuron_example.py`, if the edited file is
     `learn/neural-networks.qmd`;
   - `python3 scripts/check_transformer_path_lengths.py`, if the edited
     file is `learn/why-transformers.qmd`;
   - report pass/fail plainly, not just "ran the checks."

12. **Summarize your pass** with five lists: prose-only changes made;
   jargon removed or newly (re-)explained; analogies kept, deleted, or
   declined, each with the gate condition that decided it; flagged
   technical (MEANING) changes, each with its before/after and
   verification status; and production narration removed. Name any
   concept that resisted simplification without losing accuracy, rather
   than silently leaving it dense.

## Never do

- Never silently ship a MEANING edit because the earlier wording was
  "approved" — approval covered the wording at the time, not immunity
  from a later correction. `CLAUDE.md` itself says as much: do not
  preserve an inaccurate sentence merely because it appeared in an
  earlier rule.
- Never remove a claim ID or its citation without flagging it.
- Never invent a source, timestamp, or citation detail to support an
  edit — mark it unverified instead, exactly as the rest of this
  repository does.
- Never touch `_includes/*.qmd`, the JavaScript/CSS assets, or any
  verification script's checking *logic* as a side effect of a prose
  pass — if a script's regex needs to change because you changed the
  text it parses, that is a MEANING-adjacent change and belongs in your
  flagged list, done deliberately, not incidentally.
- Never reintroduce production or planning commentary into reader-facing
  text.
- Never mention teaching level, audience, or these authoring instructions
  anywhere in reader-facing text.
- Never add a "Think of it this way" box, or any other repeated intuition
  callout, as a structural template. An analogy earns its place by
  passing the four-condition gate, not by the section being difficult.
- Never write "as you know," "recall," or similar language that assumes
  the reader remembers something solely because it appeared earlier.
- Never name or assume a specific profession, degree, or field as the
  course's audience in reader-facing text.
- Never run `git commit`, install anything, or edit files outside
  `learn/*.qmd` (and the specific verification scripts named in rule 11,
  only to re-run them, not to change their checking logic).

## Worked example

This is the exact risk this Skill exists to catch — a plausible-sounding
edit that is quietly wrong.

> **Before (a draft edit under consideration):** "A logit is just the
> log-odds of a token being chosen, the same thing you compute in a logit
> regression."
>
> **Classification: MEANING.** This is not a prose tweak — it asserts
> that the machine-learning "logit" *is* the statistics log-odds
> transform. It is not (see `sources/claims.csv`, claim S-09, and
> `CLAUDE.md`'s PR8).
>
> **Verification:** checked against claim S-09, which states the two are
> "not interchangeable" and explains the direction of the map is
> reversed. The draft edit contradicts an existing, sourced claim rather
> than merely restating it more casually.
>
> **Correct edit:** "In this course, 'logit' means the raw, unnormalized
> real-valued score the network outputs for a candidate token before
> softmax — not the statistics term `logit(p) = log(p/(1-p))`, the
> log-odds transform of a probability already in [0,1]. Statistics' logit
> takes a probability and returns a real number; here we start with a
> real number (the score) and softmax turns it into a probability. The
> exact relationship holds only for differences: `log(p_i/p_j) =
> (z_i - z_j)/T`, and with exactly two candidates `logit(p_1) =
> (z_1 - z_2)/T`, which is `z_1 - z_2` only at `T = 1`. An individual
> score `z_i` is not `logit(p_i)`."
>
> **Outcome:** the corrected wording matches claim S-09 and PR8. Because
> this changed the meaning of an existing sentence rather than only its
> phrasing, it is reported under "Flagged technical changes," not applied
> silently.

# Practical guide specification (planning document — spec only)

This is a **specification** for a future website module on practical
Claude Code usage for empirical research. It is not the guide itself; no
`learn/*.qmd` or other public page for this content is created in this
batch.

## Provenance

The sibling coordination plan (`ai_course_coordination_starter/00_MASTER_PLAN.md`,
read for context only, never copied into this repository) has no section
literally titled "practical guide." Its closest material is Phase 3
("Session 2": project folders and paths, the terminal, VS Code and
Markdown, Git, permission decisions, task specifications and acceptance
criteria, verification standards, a controlled workflow demonstration) and
Phase 5's handoff memo. Overlap with this spec's seven topics below is
real but partial — task selection ≈ task specifications, tools ≈
permission decisions, verification ≈ verification standards — three of
seven. Prompting, context, token/model efficiency, privacy as its own
topic, and handoffs as a within-session concept are genuinely **new
scope** for this batch, stated here plainly rather than implied to already
exist in that plan.

Explicitly out of scope for this module, when built: WSL, VS Code, and Git
installation mechanics — those remain the coordination plan's territory,
not this course's.

## Sections

**1. Task selection.** What kinds of research tasks are and are not a good
fit for an agentic coding assistant. Draws on the same "coding is
verifiable" argument already used in the agent-bridge material
(`docs/live-talk-storyboard.md`, segment 20), extended to concrete research
examples (data cleaning, a well-specified estimation script) versus poor
fits (anything requiring judgment the assistant cannot verify against
ground truth).

**2. Prompts.** Per precision rule PR9: qualify every prompting
recommendation by task, model, provider, and documentation date where
appropriate. Do not turn one vendor's current guidance, or one model's
current behavior, into a universal or permanent rule — this is exactly the
error PR9 exists to prevent, and it is a particular risk in a section that
gives concrete advice.

**3. Context.** Ties directly to correction A: training changes
parameters; system instructions, retrieved information, tool results, and
other supplied state change inference-time context. This section explains
what a researcher is actually doing when they add a file, a system
prompt, or a tool result to a session — filling a context window, not
teaching the model anything permanent.

**4. Token and model efficiency.** Practical budgeting: what consumes
context, when to start a fresh session, and how model choice (a smaller,
faster model for a bounded task versus a larger one for open-ended
reasoning) trades off cost against capability — again qualified per PR9,
not stated as a fixed rule.

**5. Tools.** The permission model: what a tool call is (per PR5's
corrected framing — generated structured output that surrounding software
interprets and executes, not the model directly acting), and why a human
checkpoint on consequential actions is a design choice, not a limitation
to work around.

**6. Verification.** Worked example: this repository's own
`scripts/verify.sh` and its checks. Per PR6: a passing check is evidence
that the specified checks passed, not proof that the underlying
specification, research design, or resulting number is correct — the
distinction this whole repository's own verification discipline is built
around.

**7. Handoffs.** How to leave a piece of work in a state someone else (or
a future session) can pick up: the `docs/decisions.md` / `docs/build-log.md`
convention already in use in this repository, generalized as a practice.
Preserves the **milestone-based planning convention** this course's own
production has used throughout (`docs/decisions.md`'s dated rows,
`docs/build-log.md`'s per-task entries, `docs/milestone-timeline.md`'s
section-level rollup) — the guide should teach this convention by pointing
to this repository as a working example, not by inventing a different one.

## Verification approach, when built

Numerical or code-based claims in this module (if any — most of this
content is procedural, not mathematical) would be checked the same way
the rest of this repository checks them: a standalone script under
`scripts/`, run by `scripts/verify.sh`, never a hand-verified number taken
on faith.

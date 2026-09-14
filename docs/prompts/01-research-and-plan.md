# Task 01: Research and plan the LLM-to-agents course

## Mission

Prepare a source-grounded implementation plan for a Quarto website and Reveal.js
slide deck supporting a 45-minute talk for PhD economists:

**From LLMs to agents: what the model is, how it is built, and how it begins to act**

This run is for research, synthesis, and planning only. Do not create, edit,
move, or delete project files. Do not install Skills, plugins, MCP servers,
packages, browser extensions, or other software. Do not initialize or modify a
remote repository. Present the complete plan for external review, then stop.

The human product owner is learning this material and cannot independently
verify every technical claim. Source traceability and technical accuracy are
therefore non-negotiable.

## Audience and purpose

The audience consists of PhD economists in the Infrastructure Sector of the
Inter-American Development Bank. They understand probability, maximum
likelihood, optimization, linear algebra, multinomial logit, and empirical
research, but most are not machine-learning researchers or software engineers.

This talk is conceptual preparation for a later intensive Claude Code workshop.
It should demystify LLMs and agents without becoming a Claude Code tutorial.
Do not cover installation, WSL, Git, or detailed coding-agent workflows in this
talk.

The live talk should be intuitive, precise, and self-contained. The website
should also provide deeper mathematical extensions for participants who want
them.

## Product architecture

Plan for these two connected products:

1. A primary Reveal.js deck that can be presented coherently in about 45
   minutes.
2. A Quarto website containing the deck, annotated resources, source mapping,
   and optional "Go deeper" pages with fuller mathematics and explanations.

The presentation is a carefully selected route through a deeper website. Do not
remove mathematics from the course. Layer it.

## Timing and narrative

Target:

- Opening and motivating question: about 2 minutes.
- What an LLM is and how it is built: about 32–34 minutes.
- The bridge from LLMs to agents: about 9–11 minutes.
- Closing mental model: about 1 minute.

A small overrun is acceptable, but the planned spoken content should not exceed
approximately 48 minutes.

The live narrative should answer, in order:

1. What goes into an LLM?
2. What does it predict?
3. What is learned during training?
4. What is a transformer, and what does attention do?
5. How does the trained model generate an answer?
6. How does a base model become an assistant?
7. Why do tokens, finite context, stochasticity, and hallucinations matter?
8. What must be added to move from an LLM to an agentic system?
9. Why do tools, feedback, permissions, stopping conditions, and verification
   matter?

## Required live concepts

The live deck must make attendees familiar with, and able to distinguish:

- training data;
- tokens and tokenization;
- token IDs;
- embeddings;
- parameters or weights;
- neural-network layers and nonlinear transformations;
- transformer;
- transformer block;
- attention;
- attention head;
- feed-forward or MLP layer;
- context window;
- logits;
- softmax;
- temperature;
- sampling versus choosing the maximum;
- next-token prediction;
- negative log likelihood or cross-entropy;
- maximum likelihood;
- gradient descent;
- backpropagation at an intuitive level;
- pretraining;
- post-training;
- base model;
- assistant;
- retrieval;
- tool call;
- project instructions or supplied memory/state;
- workflow;
- agent;
- agent loop;
- Skills as reusable instructions/resources supplied at inference time, not
  changes to model weights.

Make the hierarchy explicit:

- an LLM is the trained model;
- a transformer is the neural-network architecture inside most modern LLMs;
- attention is a central mechanism inside a transformer block;
- an assistant combines the model with post-training and surrounding product
  instructions;
- an agentic system surrounds the model with tools, state, permissions, and a
  feedback loop.

## Mathematical depth and layering

The live deck should be mathematically literate but selective.

Use intuition first, then formal notation when it materially improves
understanding. In the live deck, require only:

1. the softmax equation, explicitly connected to multinomial logit;
2. the negative-log-likelihood training objective, explicitly connected to
   maximum likelihood.

A simplified attention weighted-average equation may appear if it improves the
story. Do not require the audience to parse the full query-key-value matrix
equation live.

Explain embeddings, gradient descent, backpropagation, transformer blocks, and
attention accurately and intuitively in the talk. Put fuller notation,
derivations, numerical examples, matrix dimensions, and limitations of the
econometric analogies in linked website extensions.

Each core concept should use this sequence where appropriate:

1. the problem the mechanism solves;
2. a tiny concrete example;
3. the mathematical object;
4. the intuition in plain language;
5. what the concept explains about real LLM or agent behavior;
6. a link to the deeper website treatment.

The website extensions should include, where relevant:

- a numerical softmax and sampling example;
- temperature and odds;
- cross-entropy and maximum likelihood;
- a small computational graph explaining backpropagation;
- embeddings and vector similarity;
- transformer blocks;
- queries, keys, values, masking, multi-head attention, residual connections,
  and feed-forward layers;
- context allocation and compaction;
- pretraining and post-training;
- model versus assistant versus workflow versus agent;
- tool schemas, environmental feedback, and stopping conditions.

## Agent bridge

Use the progression:

1. base model;
2. instruction-following assistant;
3. augmented LLM with retrieval, tools, and state;
4. fixed workflow;
5. agent operating in a loop.

Show one concrete loop:

objective and context
→ model proposes a structured tool call
→ permission/control layer evaluates it
→ external software executes it
→ the environment returns evidence
→ that evidence enters the next model call
→ the model continues, asks for help, or stops.

Explain why coding is especially suitable for agentic work: code can be run,
errors can be observed, tests can provide feedback, and file changes can be
inspected. Also explain why a successful command or fluent completion is not
proof that the research result is correct.

## Primary sources and research protocol

Use original, authoritative, widely respected sources. Begin with this source
hierarchy:

1. Andrej Karpathy, **Deep Dive into LLMs like ChatGPT**, as the principal
   narrative anchor for data, tokenization, pretraining, post-training, and
   model behavior.
2. 3Blue1Brown, **Transformers, the tech behind LLMs** and **Attention in
   transformers, step-by-step**, as the main visual and intuitive supplement
   for transformers, embeddings, and attention.
3. Anthropic, **Building Effective AI Agents**, as the main conceptual anchor
   for augmented LLMs, workflows, tools, environmental feedback, and agents.
4. Official Claude Code and Anthropic documentation for current,
   product-specific explanations of tools, context, Skills, permissions, and
   agent behavior.
5. Foundational papers, including **Attention Is All You Need**, only where
   needed to verify a technical statement not adequately supported by the
   general-audience anchors.

Use original sources rather than third-party summaries whenever possible.
Do not reproduce transcripts, long quotations, screenshots, diagrams, or
animations without confirming reuse rights. Plan to redraw original diagrams
in our own visual language.

For each planned substantive slide or website module, identify:

- the main claim or explanation;
- original source;
- exact chapter, page, section, or video timestamp;
- whether the source directly supports the claim or is being used for an
  inference;
- confidence and any technical caveat.

Cap the core source set at approximately 8–10 sources unless an additional
source is necessary to resolve a real disagreement. Do not conduct an
unbounded literature review.

Do not load entire video transcripts into the main conversation. Delegate
targeted source reconnaissance to read-only subagents and return concise,
timestamped notes.

## Interactive elements

Plan two small browser-based interactive elements:

1. **Softmax and sampling laboratory**
   - user changes 3–5 logits and temperature;
   - probabilities update;
   - user can draw one token or repeated draws;
   - empirical frequencies can be compared with theoretical probabilities.

2. **Agent-loop step-through**
   - shows the boundaries among the model, agent harness, permissions, tools,
     operating environment, returned evidence, and stopping decision.

A tokenization illustration may be included if it remains small and robust.
Do not propose decorative interactivity.

Prefer Quarto-native or browser-side solutions that render to a static site.
Do not require a live API, confidential data, or a persistent server.

## Skills and plugin reconnaissance

Research whether existing Claude Code Skills or plugins would materially
improve this workflow.

Search in this order:

1. the official Anthropic Claude Code marketplace;
2. `anthropics/skills`;
3. `anthropics/claude-plugins-official`;
4. Anthropic's Claude Code demo marketplace;
5. reputable community repositories only if the official sources do not cover
   a clearly useful need.

Look specifically for capabilities related to:

- Quarto or Reveal.js authoring;
- instructional or technical writing;
- frontend or visual design;
- accessibility review;
- static-site or web-app testing;
- screenshot or browser-based visual verification;
- link checking;
- source/citation mapping;
- research-source review;
- Skill creation or evaluation.

Do not install anything. Do not add a marketplace. Do not clone a repository.

For at most five serious candidates, report:

- exact name and source;
- owner/maintainer;
- official, partner, or community status;
- what files, scripts, hooks, MCP servers, or external dependencies it includes;
- what permissions or network access it would require;
- license;
- last meaningful update if readily available;
- concrete value for this project;
- overlap with native Claude Code or simple project instructions;
- security and maintenance risks;
- recommendation: install later, adapt locally, or do not use.

Prefer a small project-level Skill we can inspect and write ourselves when the
need is mostly a repeatable instruction set. A large plugin is not automatically
better. It is acceptable to conclude that no external Skill should be
installed.

## Model routing and token discipline

The main session is launched with `opusplan`.

Use models deliberately:

- **Opus**: curriculum architecture, difficult conceptual synthesis, resolving
  conflicting technical explanations, and the final high-stakes technical
  audit.
- **Sonnet**: later implementation of Quarto, CSS, JavaScript, speaker notes,
  source-map files, and revisions.
- **Haiku**: bounded source discovery, repository inventory, candidate-Skill
  discovery, link/status checks, and other repetitive read-only work.

During this planning run:

- keep the main Opus context clean;
- delegate source scouting and Skill scouting to separate read-only Haiku
  subagents;
- ask subagents to return concise structured summaries, not raw page dumps;
- use no 1-million-token model variant;
- use no `max` effort;
- avoid duplicate searches;
- stop researching once the required content can be source-grounded;
- report if model or tool restrictions prevent the requested routing.

Later, implementation should use Sonnet, with an independent Opus technical
review and a bounded Haiku verification pass.

## Expected implementation deliverables after plan approval

The eventual implementation should include at minimum:

- `_quarto.yml`
- `index.qmd`
- `slides/llms-to-agents.qmd`
- `learn/tokens-context.qmd`
- `learn/softmax-sampling.qmd`
- `learn/training.qmd`
- `learn/transformers-attention.qmd`
- `learn/posttraining.qmd`
- `learn/agents.qmd`
- `resources.qmd`
- `sources/source-map.md`
- `README.md`
- supporting JavaScript and CSS
- a concise `CLAUDE.md`
- project-level verification commands or scripts

The deck must contain speaker notes, cumulative timing, unobtrusive citations,
and links to deeper pages. The site must have an annotated resource list.
No placeholders, outline-only slides, empty sections, or unsupported factual
claims should remain in a completed first draft.

## Verification strategy to include in the plan

The plan must specify how implementation will verify:

- `quarto render` succeeds;
- the website and Reveal.js deck open correctly;
- internal links work;
- external source links resolve;
- both interactives function;
- slides remain legible at presentation resolution;
- essential content does not depend on an external service during the talk;
- each substantive claim is represented in the source map;
- every technical term is defined before or when first used;
- estimated talk time is approximately 45 minutes;
- website extensions contain the deeper mathematics omitted from the live deck;
- diagrams and wording are original and do not reproduce source material
  beyond fair quotation limits;
- an independent technical review identifies unsupported, misleading, or
  oversimplified claims.

## Required output for this planning run

Return one structured plan containing:

1. **Repository audit**
   - what currently exists;
   - available tools;
   - constraints that affect implementation.

2. **Source strategy**
   - core sources;
   - why each source is being used;
   - targeted chapters/timestamps;
   - technical gaps requiring additional verification.

3. **Narrative and slide sequence**
   - slide or segment title;
   - teaching objective;
   - core content;
   - visual or interactive treatment;
   - live mathematics;
   - source;
   - estimated time;
   - cumulative time.

4. **Website extension map**
   - page structure;
   - deeper mathematical content;
   - relationship to the live deck.

5. **Interactive design**
   - behavior;
   - implementation approach;
   - fallback if browser interactivity fails;
   - verification approach.

6. **Skills/plugin shortlist**
   - no more than five candidates;
   - security and value assessment;
   - explicit install/adapt/reject recommendation.

7. **Model-routing execution plan**
   - which tasks use Opus, Sonnet, or Haiku;
   - how contexts will remain separate;
   - how unnecessary token use will be avoided.

8. **Proposed repository tree**
   - exact planned files and directories.

9. **Implementation stages**
   - small vertical slice first;
   - full content build;
   - technical review;
   - visual and timing review;
   - final verification.

10. **Acceptance criteria and commands**
    - exact checks the later implementation will run.

11. **Risks and unresolved decisions**
    - distinguish true blockers from choices that can be made provisionally.

Do not implement. Do not install. Do not ask broad or avoidable questions.
Make reasonable provisional choices and mark them. Present the plan for
external review and stop.

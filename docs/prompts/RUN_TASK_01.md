# Run Task 01 in Claude Code

## 1. Open the project in WSL

```bash
cd ~/projects/from-tokens-to-agents
mkdir -p course-site/docs/prompts
cd course-site
code .
```

## 2. Create the prompt file

In VS Code Explorer:

1. Open `docs/prompts/`.
2. Create `01-research-and-plan.md`.
3. Paste the complete contents of `01_RESEARCH_AND_PLAN_PROMPT.md`.
4. Save.

## 3. Start Claude Code in the Enterprise account

From the VS Code terminal:

```bash
cd ~/projects/from-tokens-to-agents/course-site
claude --model opusplan --permission-mode plan
```

Inside Claude Code:

```text
/status
```

Confirm the Enterprise organization. Then set:

```text
/effort high
```

Do not use `max` effort or a `[1m]` model.

Optionally name the session:

```text
/rename llm-course-research-plan
```

## 4. Start Task 01

Paste this short instruction:

```text
Read @docs/prompts/01-research-and-plan.md and execute it exactly.

This is Phase A only: source research, Skills/plugin reconnaissance, synthesis,
and an implementation plan. Use read-only subagents and the model routing
specified in the file. Do not edit project files, install anything, add a
marketplace, clone repositories, or begin implementation.

When the complete plan is ready, present it for external review and stop.
```

## 5. Permission decisions during this run

Appropriate to approve:

- `WebSearch`
- `WebFetch` for relevant public sources
- read-only file inspection
- read-only Git commands such as `git status` and `git log`
- read-only subagents

Do not approve during Task 01:

- file writes or edits
- plugin or Skill installation
- marketplace additions
- `git clone`
- package installation
- MCP server installation or configuration
- `git push`
- deletion or file movement

## 6. Stop at the plan

Do not approve implementation when Claude presents the plan.

Copy Claude's complete plan and return it to ChatGPT for review. The next prompt
will be written only after the plan, source choices, Skill shortlist, and token
strategy have been checked.

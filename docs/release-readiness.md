# Release readiness (public review draft, deployed 2026-09-16)

## 30-minute release candidate (2026-09-16, local commit, not deployed)

One bounded correction pass, applied after the public review draft was
deployed. **These corrections exist only in the local repository until
`main` is pushed and the publish workflow is run; the live site still
serves commit `72850bf`.**

What changed:

- Talk length: 30-minute slot, 28.0 minutes of prepared material across
  24 slides plus a 2-minute reserve. The "ChatGPT-like product" slide is
  now a backup slide (class `.backup`, labeled on the slide, placed after
  the closing slide, "Time: backup" in the guide); the runnable-model
  slide carries the product-around-the-model point in one sentence. The
  guide's per-slide estimates and running totals were rewritten, and
  `scripts/check_slides_guide.py` now parses backup slides and enforces
  28 + 2 = 30.
- Narrative order: "What happens when you type" (the inference loop) now
  precedes reasoning-oriented models in the deck, the guide, and the
  Short Story, so "thinking longer" is explained after the reader knows
  what one generation step is.
- Memorization: the base-model slide, its notes, and Short Story §6 now
  say that a base model is not a reliable database but can memorize and
  reproduce training passages, citing Carlini et al. (2021), new claim
  row S-87 (87 rows total).
- Attention: the Short Story and the attention slide give the complete
  step sequence (query, key, score, softmax, value, weighted combination;
  learned matrices versus computed weights); the intuition figure's
  weights label no longer overlaps the updated-representation box and
  its caption defines value vectors. The tiny-network caption no longer
  contains TeX (raw HTML captions do not go through MathJax).
- Reasoning visibility is qualified (what is shown depends on the product
  and is not a guaranteed faithful record); R1-Zero is described as
  reinforcement learning applied directly to the pretrained base model.
- Slide legibility: chip, card, and legend text enlarged in
  `assets/css/slides.scss`; the deck's hand-written HTML blocks (product
  box, tokens chip row, three lifecycle lists, tool-call step grid) are
  wrapped in raw-HTML fences because Pandoc otherwise parsed their
  contents as markdown (the product chips were rendering as inline text
  with broken borders, and straight quotes in code were being turned into
  typographic quotes).
- Public descriptions (Home, README, deck closing slide) say 30 minutes
  and "24 slides in the prepared route plus one backup slide". The
  ` bank` token is quoted as code (`␣bank`) wherever it appears.

Observed results, 2026-09-16:

- `bash scripts/verify.sh`: all 16 steps pass (87 claim IDs; 13 Short
  Story figures in the new order; 24 prepared + 1 backup slide reconcile
  with the guide at 28.0 + 2 = 30 minutes; Sources page in sync).
- Headless Chromium, deck at 1280×720: 25 sections, none overflowing,
  smallest text 16.9 px (source footers), body text 28 px; the tool-call,
  post-training, thinking-longer, corpus, tokens, pretraining, agent-loop,
  coding-agent, and backup product slides were inspected from
  screenshots after the CSS and fence changes.
- Headless Chromium, site: the Short Story renders the corrected
  attention and tiny-network figures (caption shows HTML italics, no
  literal TeX), the three moved section anchors exist, glossary previews
  work on hover and keyboard focus, no failed requests at the root or
  under a sub-path, no horizontal overflow at 390 px. A lesson page
  renders 41 MathJax equations with no raw delimiters (MathJax loads from
  its CDN on the website; the deck has no CDN dependency).
- Backup PDF regenerated: `dist/llms-to-agents.pdf`, 25 pages (not
  tracked; `dist/` is ignored).

Remaining limitations:

- The 28-minute estimate is unmeasured: no timed rehearsal has been
  done. Per-slide estimates are the author's judgment.
- Every PDF page was not inspected individually.
- `CLAUDE.md` still describes the talk as 35–40 minutes; it is a
  contributor instruction file and was outside this pass's scope.
- The editorial backlog below (Short Story tone) is unchanged; no general
  style revision was made.

## Deployment record

- Repository: <https://github.com/LeonelBorjaPlaza/llm-to-agents>, public,
  issues enabled, default branch `main`.
- Site: <https://leonelborjaplaza.github.io/llm-to-agents/> (GitHub Pages,
  build type "workflow"). First successful deployment: run
  <https://github.com/LeonelBorjaPlaza/llm-to-agents/actions/runs/35056786998>
  on commit `fc3b823` ("Prepare public review draft"), 2026-09-16. Later
  deployments are listed in the repository's Actions tab; each records the
  commit it deployed.
- Live checks performed in headless Chromium against the public address
  on 2026-09-16: Home with the working-draft notice and the
  "Suggest a correction" link; the Short Story with all thirteen figures
  visible; a claim marker linking to the matching entry on the public
  Sources page; a nested lesson with page references rendered as links;
  glossary previews on hover and on keyboard focus; the glossary (98
  entries); the resources page's video route; the speaking guide; the
  25-slide presentation with its attention figure visible and its
  closing links back to the site; no failed asset requests, no 4xx or 5xx
  responses, no console errors; and phone-width pages (390 px) without
  horizontal overflow. HTTP 200 confirmed for the root, the Short Story,
  a lesson, the glossary, the Sources page, the resources page, the deck,
  the guide, and a Reveal asset under `/llm-to-agents/`.
- To publish an update: edit → `bash scripts/verify.sh` → commit → push
  `main` → `gh workflow run publish.yml --repo LeonelBorjaPlaza/llm-to-agents --ref main`.
  Deployment is manual on purpose.

## Candidate checklist before deployment (2026-09-15)

Factual checklist for the working-draft release candidate: the website,
the live presentation (`slides/llms-to-agents.qmd`), and its speaking
guide (`slides/speaking-guide.qmd`). Items are separated into checked,
failed, and untested. "Checked" means a script or a headless-browser run
in this environment confirmed it; it is not a substitute for a human
reading the pages or rehearsing the talk.

## Checked

- Full `quarto render` succeeds with no warnings (Quarto 1.10.18).
- Scripted suite (`bash scripts/verify.sh`, 16 steps): render, internal
  links and anchors, source reconciliation (87 claim IDs, root pages and
  slides included), six numerical checks, glossary and resources checks,
  origin-root asset-path check, Short Story figure check (13 figures in
  order, no SVG broken by markdown parsing, every figure include used),
  deck-to-guide reconciliation (24 prepared slides plus 1 backup, 28.0
  prepared minutes plus a 2-minute reserve), the Sources page check, and
  the static offline check of the deck. All 16 pass (re-run 2026-09-16
  after the 30-minute pass).
- Deck rendered in headless Chromium at 1280×720: 25 slides, none
  overflowing the canvas, smallest visible text about 17 px (source
  footers) with body text at 28–30 px; every SVG figure visible.
  Screenshots for each slide were captured for review (see below).
- Website in headless Chromium, served at the server root and under a
  sub-path (`/course-prefix/`): Home, Short Story, a nested lesson, the
  glossary, the deck, and the guide load with no failed requests and no
  4xx or 5xx responses; the eight Short Story SVG figures render at
  visible sizes; the custom stylesheet (chips, callouts, tooltips) is
  compiled into the theme; glossary previews appear on hover and on
  keyboard focus, hide on mouse-leave and Escape, and clicking navigates
  to the correct glossary anchor; at a 390 px viewport there is no
  horizontal overflow.
- PDF fallback of the deck produced through Reveal's print view in
  headless Chromium: `dist/llms-to-agents.pdf`, 25 pages (regenerated
  2026-09-16 after the 30-minute pass).
- Local preview archive of the rendered public site:
  `dist/course-preview.zip` (rendered files only; `dist/` is ignored by
  Git).
- The new deck has no runtime dependency on a CDN: the unused Reveal
  math plugin was disabled (`html-math-method: plain`), so the static
  offline check passes. Reveal's own scripts and styles load from the
  site's `site_libs/` folder.
- Publication workflow: `.github/workflows/publish.yml`, manually
  triggered (`workflow_dispatch`), renders with Quarto 1.10.18, runs the
  complete `scripts/verify.sh` suite (standard-library Python only),
  uploads `_site/` as the Pages artifact, and deploys it with the official
  Pages actions. Run successfully on 2026-09-16 (see the deployment
  record above).
- Privacy scan of the tracked files: no credentials, environment files,
  or private coordination material; the only personal identifier is the
  Git author name on commits.

## Failed

- None of the release candidate's checks fail. The historical failure of
  the three-slide prototype's CDN dependency no longer applies: that deck
  was replaced at the same public path.

## Next iteration (editorial backlog, not blockers)

Recorded from the owner's review before publication: parts of the Short
Story could still be more intuitive, more naturally written, and simpler
without losing precision. These are next-iteration improvements to be made
with reviewers' feedback, not reasons to withhold the working draft.

## Untested

- A human has not read the rendered pages in a browser since the figure
  and stylesheet fixes, and the presentation has not been rehearsed or
  given to an audience. The timing estimates, including the 28-minute
  prepared total, are not measured.
- Offline use: the deck was verified only statically (no external
  references) and by serving the `_site` folder over a local HTTP server.
  Opening the folder from disk with the network disabled was not tested.
  Treat the archive as a locally served package, not as verified offline
  capable.
- The PDF was rasterized for one page and opened for a page count; every
  page was not inspected.
- Screen-reader behavior of the figures (aria labels and descriptions
  exist; they were not tested with assistive technology).

## Activation steps (performed on 2026-09-16)

1. Destination confirmed by the owner: account LeonelBorjaPlaza,
   repository `llm-to-agents`, public.
2. Repository created with the GitHub CLI and `main` pushed.
3. Pages configured through the REST API with build type "workflow".
4. Workflow "Publish site to GitHub Pages" dispatched on `main` and
   watched to completion (build and deploy jobs succeeded).
5. Live site verified as recorded above.
6. Public address added to README, the deck's closing slide, and the
   speaking guide; internal links remain relative.

## Publication review notes

- Everything tracked in Git is now public, including `docs/` (planning
  prompts, build log, decisions, a first-learner review) and `sources/`
  (the claim ledger). Before the first push the tracked files, the
  commits reachable from `main`, files removed in history (none), and the
  rendered output were scanned: no credentials, tokens, environment
  files, local settings, or private coordination material; the only
  personal identifier is the Git author name.
- No license file exists and no institutional logo or endorsement is
  present; neither was added, because no authorization exists.
- Local QA artifacts (screenshots, the Playwright virtualenv) live outside
  the repository; `dist/` is ignored.

## Screenshots captured for review (outside the repository)

`/tmp/claude-1000/-home-leonelb-projects-from-tokens-to-agents-course-site/2a4f32e4-ebf3-4408-a7af-a9c6af28daf3/scratchpad/qa/shots/`:
one PNG per slide (`slide-NN-<id>.png`), Home at desktop and phone
width, the Short Story top and its attention figure, the glossary
tooltip on hover, the narrow-width lifecycle and tool round trip, and one
rasterized PDF page. These are session files and will not survive the
session; regenerate with the QA scripts described in
`docs/build-log.md` if needed.

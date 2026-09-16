# Release readiness (Batch 6 candidate, 2026-09-15)

Factual checklist for the working-draft release candidate: the website,
the live presentation (`slides/llms-to-agents.qmd`), and its speaking
guide (`slides/speaking-guide.qmd`). Items are separated into checked,
failed, and untested. "Checked" means a script or a headless-browser run
in this environment confirmed it; it is not a substitute for a human
reading the pages or rehearsing the talk.

## Checked

- Full `quarto render` succeeds with no warnings (Quarto 1.10.18).
- Scripted suite (`bash scripts/verify.sh`, 15 steps): render, internal
  links and anchors, source reconciliation (86 claim IDs, root pages and
  slides included), six numerical checks, glossary and resources checks,
  origin-root asset-path check, Short Story figure check (13 figures in
  order, no SVG broken by markdown parsing, every figure include used),
  deck-to-guide reconciliation (25 slides, 38.0 estimated minutes), and
  the static offline check of the new deck. All 15 pass.
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
  headless Chromium: `dist/llms-to-agents.pdf`, 25 pages.
- Local preview archive of the rendered public site:
  `dist/course-preview.zip` (rendered files only; `dist/` is ignored by
  Git).
- The new deck has no runtime dependency on a CDN: the unused Reveal
  math plugin was disabled (`html-math-method: plain`), so the static
  offline check passes. Reveal's own scripts and styles load from the
  site's `site_libs/` folder.
- Publication workflow prepared but not run:
  `.github/workflows/publish.yml`, manually triggered
  (`workflow_dispatch`), renders with Quarto 1.10.18, runs the repository
  checks (standard-library Python only), uploads `_site/` as the Pages
  artifact, and deploys it with the official Pages actions.
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
  given to an audience. The timing estimates are not measured.
- Offline use: the deck was verified only statically (no external
  references) and by serving the `_site` folder over a local HTTP server.
  Opening the folder from disk with the network disabled was not tested.
  Treat the archive as a locally served package, not as verified offline
  capable.
- The PDF was rasterized for one page and opened for a page count; every
  page was not inspected.
- Screen-reader behavior of the figures (aria labels and descriptions
  exist; they were not tested with assistive technology).
- The GitHub Actions workflow has not run, because no remote exists yet.

## Activation steps (not performed; require authorization)

1. Choose the destination repository and confirm its visibility policy.
   Missing at the time of writing: GitHub account or organization,
   repository name, and whether the site should live under a project path
   (`https://<account>.github.io/<repository>/`). The site is built with
   relative links and works under such a path without configuration
   changes.
2. Create the remote and push the `main` branch (`git remote add`,
   `git push`). Not done here.
3. In the repository settings, under Pages, set the build and deployment
   source to "GitHub Actions".
4. Run the workflow "Publish site to GitHub Pages" from the Actions tab
   (it is `workflow_dispatch` only). The deploy job publishes the
   `github-pages` environment; the URL appears in the job summary.
5. Open the published root page and one nested page
   (`learn/agents.html`) and confirm styles, figures, glossary previews,
   and the link from the deck's last slide back to the site.
6. Only then add the public URL to the site (there is no URL or QR code
   in the materials yet, on purpose).

## Publication review notes

- Everything tracked in Git would be public in a public repository,
  including `docs/` (planning prompts, build log, decisions, a first-learner
  review) and `sources/` (the claim ledger). They contain no credentials
  or private institutional material, but they are working documents;
  decide whether they should be public before choosing repository
  visibility.
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

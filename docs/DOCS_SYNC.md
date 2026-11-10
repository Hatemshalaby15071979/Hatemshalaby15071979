# Docs-sync engine

An automation that keeps the **visitor-facing status** of every repo current, the
moment a release ships — without prompting an agent each time. When a repo
publishes a release, its `README.md` and `index.html` get their status block
refreshed from **proven facts** and a pull request is opened for review.

This is the "quantum entanglement" requested: a status change in one place is
reflected in the docs automatically, across all opted-in GitHub repos.

## Trigger

`on: release: { types: [published] }` — i.e. **only on release/tag**, never on
every push. A plain commit does not touch the docs.

## What it updates

Only the delimited **status block** inside each doc:

```markdown
<!-- docs-sync:start -->
**Version 2.1.1 — released 10 November 2026.** 465 automated tests pass, the
code is 51.55% covered, and all CI checks are green.
<!-- docs-sync:end -->
```

Everything outside the markers is hand-authored prose and is **never** rewritten.
Standalone tokens (`@DOCS_SYNC_VERSION@`, `@DOCS_SYNC_DATE@`, `@DOCS_SYNC_TESTS@`,
`@DOCS_SYNC_COVERAGE@`, `@DOCS_SYNC_CI@`) are also replaced wherever they appear
(e.g. inside a badge URL), so a repo can opt in at any granularity.

If a file has no markers and no tokens, it is left alone — the engine is opt-in
per file.

## Where the facts come from (never invented)

| Fact | Source |
|---|---|
| `version` | the release tag (real) |
| `release_date` | the release's `published_at` (real) |
| `ci_status` | the checks API on the release commit — **if not green, the sync aborts** (no fake green) |
| `tests_passed`, `coverage` | the repo's `_docs_profile.json` (the human-verified baseline); a future release that runs the suite can override |

## How to onboard a repo

1. Add the markers around the existing status sentence in `README.md` and
   `index.html` (and `marketing/index.html` if present).
2. Add a `_docs_profile.json` with the human-verified facts and, optionally, a
   `status_template` / `status_template_html` to keep your voice:
   ```json
   {
     "name": "Helix Education",
     "repo": "Hatemshalaby15071979/Helix-Education",
     "status_template": "**Version @DOCS_SYNC_VERSION@ — released @DOCS_SYNC_DATE@.** @DOCS_SYNC_TESTS@ automated tests pass@COVERAGE_FRAGMENT@, and @DOCS_SYNC_CI@.",
     "status_template_html": "<p class=\"status\"><strong>Version @DOCS_SYNC_VERSION@ — released @DOCS_SYNC_DATE@.</strong> @DOCS_SYNC_TESTS@ automated tests pass@COVERAGE_FRAGMENT@, and @DOCS_SYNC_CI@.</p>",
     "facts": {
       "version": "2.1.1",
       "release_date": "10 November 2026",
       "tests_passed": 465,
       "coverage": 51.55,
       "ci_label": "all CI checks are green"
     }
   }
   ```
3. Add `.github/workflows/docs-sync.yml`:
   ```yaml
   name: docs-sync
   on:
     release:
       types: [published]
   permissions:
     contents: write
     pull-requests: write
   jobs:
     sync:
       runs-on: ubuntu-latest
       steps:
         - uses: Hatemshalaby15071979/Hatemshalaby15071979/.github/actions/docs-sync@master
           with:
             profile: _docs_profile.json
   ```

## Landing

The engine opens a PR (`docs/auto-sync-<version>`) and stops. A human reviews and
merges — keeping a person in the loop and matching the "show only what is proven"
rule. It never commits straight to the default branch.

## Repos opted in

| Repo | Status |
|---|---|
| L-D-Command-Center | wired |
| Study-Studio | wired |
| Helix-Education | wired |
| Helix Codex | pending (initial humanization) |
| SigmaHelix | pending (initial humanization) |
| CompliProof | pending (initial humanization) |
| SignOff | pending (initial humanization) |
| CreateLee | pending (initial humanization) |
| Portfolio | host + pending (initial humanization) |

The "pending" repos still need their one-time humanization/audit pass first; the
engine only keeps status current after that.

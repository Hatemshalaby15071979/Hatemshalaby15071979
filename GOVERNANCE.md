# GOVERNANCE.md — Operating Policy & Repo Map for the Portfolio Index

> Companion to `CONSTITUTION.md` (the *why* — philosophy and clean-code policy, which
> this file enforces operationally) and `AGENTS.md` (the agent charter + ledger).
> Read all three before acting. This file may be updated by any agent **as a logged
> governance change**; the CONSTITUTION itself is owner-only.

## 1. Repository map

This repository is more than a profile page: it is the **portfolio index** and it hosts
**shared automation that every other repository depends on**. Treat it as
infrastructure, not as decoration.

| Path | Purpose (one line) |
|---|---|
| `.github/actions/docs-sync/` | **The shared docs-sync action.** Every other repository in the portfolio calls it as `Hatemshalaby15071979/Hatemshalaby15071979/.github/actions/docs-sync@master`. On a published release it refreshes that repository's visitor-facing status block from proven facts and opens a pull request — it never commits straight to a default branch. |
| `.github/workflows/docs-sync.yml` | This repository's own caller of that action; release-triggered only, so a plain push never touches the docs. |
| `.github/workflows/secret-scan.yml` | The gitleaks secret scan. |
| `.github/workflows/ci.yml` | The root-document gate for this repository. |
| `docs/DOCS_SYNC.md` | How the docs-sync engine works, and what it refuses to do. |
| `README.md` | The profile README — rendered on the owner's GitHub profile page — and the portfolio index. |
| `index.html` | The same account as a landing page. It mirrors the README; it never forks it. |
| `_docs_profile.json` | This repository's docs-sync configuration. |

**Do not break the shared action.** Fourteen-plus repositories reference
`.github/actions/docs-sync@master` on the default branch. A change there takes effect
everywhere the next time any of them publishes a release, with no staging step. Treat
`action.yml` and `render_docs.py` as the most dangerous files in the portfolio.

## 2. Documentation policy (what belongs where)

**Root holds only the requested set** — nothing else:

| File | State | Purpose |
|---|---|---|
| `README.md` | required | The single source of truth: what this is, why it's here, how to use it — in simple English for a professional reader. Carries the Helix Solutions logo. Also the GitHub profile page. |
| `AGENTS.md` | required | Agent charter + sign-in/out ledger. |
| `CONSTITUTION.md` | required | The owner's engineering philosophy and clean-code policy (unified across every repo). |
| `GOVERNANCE.md` | required | This file: repo map, documentation policy, sync policy, archiving rules. |
| `CHANGELOG.md` | standard | Dated user-visible changes. |
| `LICENSE` / `LICENSE.md` | standard | MIT, unless the repo states otherwise. `README.md` states MIT. |
| `SECURITY.md` | standard | This repository's security policy; it already records that there is no executable code here to patch. |

**Everything else lives in `docs/`** — reports, audit logs, execution plans, research
notes, ADRs, runbooks, anything dated or one-off. No stray `.md`/`.txt` at the root.
If a document at the root is not in the table above, move it to `docs/` (or
`docs/archive/` if it is historical) and record the move in the `AGENTS.md` ledger.

## 3. Synchronization & harmony policy

The owner's rule: **the repository's actual status must match its README at all times,
locally and remotely.**

1. `README.md` is the canonical account. `index.html` mirrors it; it never forks it.
2. When reality changes, update `README.md` **first**, then mirror it to the page.
3. Every sanctioned change is committed **and pushed** to the default branch, so the
   GitHub copy, the local working copy, and any local platform that reads the repo
   all show the same truth.
4. The project table in `README.md` is the portfolio's index of record. When a project's
   status changes, this table changes in the same landing as the project's own README.
5. A number published anywhere (README, page, badge) must be reproducible from the
   repository it describes. A stale figure is removed, not left to rot.

## 4. Archiving rule

- Archive (move to `docs/archive/`), never delete: historical reports, superseded plans,
  dated audits, and one-off execution logs.
- Delete outright only regenerable artifacts: caches, build output, coverage files.
- Record every move in the `AGENTS.md` ledger with date and time.

## 5. Engineering philosophy & clean-code policy (operational summary)

The full text is `CONSTITUTION.md`. The operational reminders, enforced here:

- **Fail closed.** Missing input or missing authority is a refusal, never a default.
- **Evidence before claims.** Published numbers carry a command, a date, and an artifact.
- **No duplicates, no temp files, one file one job, every file explains itself.**
- **Secrets never enter the tree.**
- **Simple English** in code, docs, and UI, so a non-technical professional reader
  (recruiter, partner) can follow.
- **One brand mark:** the Helix Solutions logo, everywhere.

## 6. Definition of done

It works; it has a test or a documented manual check; the `AGENTS.md` ledger has an
entry; the docs reflect the new reality; no temporary file was left behind; and every
published number can be re-run to reproduce itself.

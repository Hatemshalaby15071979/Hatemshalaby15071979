# Changelog

All notable changes to the portfolio index are recorded here.
Format follows [Keep a Changelog](https://keepachangelog.com/).

This file is new as of 2026-11-27; before it existed, changes to this repository were
recorded only in the git log.

## 2026-11-27

### Added

- `AGENTS.md` — agent charter and the sign-in/sign-out ledger.
- `CONSTITUTION.md` — the owner's engineering philosophy and clean-code policy, the
  same text as in every other repository in the portfolio.
- `GOVERNANCE.md` — repo map, documentation policy, sync policy and archiving rules.
- `LICENSE` — MIT, matching the licence `README.md` already stated.
- `scripts/check_root_docs.py` — the root-document hygiene gate from `GOVERNANCE.md`
  section 2, checked in both directions. Wired into CI, with a self-test that proves it
  fails closed.
- `.github/workflows/ci.yml` — CI for this repository, which previously had workflows
  for docs-sync and secret scanning but no general CI.

### Unchanged, and deliberately so

- `.github/actions/docs-sync/` and its workflow. Every other repository in the portfolio
  calls the shared action on this default branch; it was not touched by this landing.

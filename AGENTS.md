# AGENTS.md — Agent Charter & Ledger for the Portfolio Index

> **Read order (mandatory, every landing):** `AGENTS.md` → `CONSTITUTION.md` →
> `GOVERNANCE.md` → `README.md`. Then **sign in** to the ledger below, do the work,
> **sign out**. No entry, no trust: an unlogged session's work is treated as unverified
> until someone checks it.

## 1. Who agents are here

An "agent" is any entity that reads or writes this repository — an AI model, an
automation script, or a human acting as operator. There is exactly **one supreme
authority**: the repository owner (**Hatem Shalaby**). An agent acts only on the
owner's instruction and records every landing.

## 2. The mandatory sign-in / sign-out rule

Every agent, on **every landing** (a landing = one session that ends with the agent
stopping, whether the task is finished or not), must:

1. **SIGN IN** before any write action — who, why, what will be touched, sensitive or
   network actions planned, and the **date and time from the system clock**.
2. **SIGN OUT** when the landing's work is complete or stopped — what changed, why,
   the files touched, evidence of verification, and **the current status when leaving**,
   written so the next agent can continue without re-discovery.

Fail closed: if a task cannot be completed, still sign out and state exactly what is
incomplete. Never claim verification that did not happen.

### Entry format

```
## [YYYY-MM-DD HH:MM TZ] — <agent name / model>
Task: <what was assigned>
Touched: <files created / modified / deleted / moved>
Why: <the reasoning, not just the diff>
Verification: <what was actually checked and the observed result>
Left undone: <what is incomplete, needs review, or is deferred — or "nothing">
Sensitive: <any remote writes, secrets, or destructive actions, or "none">
```

## 3. Environment facts

- **Repo:** the portfolio index. It carries the owner's GitHub **profile README** and, more importantly, the **shared `docs-sync` action** that every other repository in the portfolio calls on this default branch.
- **Owner account:** https://github.com/Hatemshalaby15071979
- **Default branch:** master
- **Why the branch name matters:** other repositories reference the shared action as `.github/actions/docs-sync@master`. Renaming this default branch breaks docs-sync everywhere at once.
- **Where it runs:** the action runs in the calling repository's own workflow, on a published release only. It refreshes the status block and opens a pull request; it never commits straight to a default branch.
- **Verification command:** `python3 scripts/check_root_docs.py` (the root-document gate; `--self-test` proves it fails closed). The action itself is rendered by `render_docs.py`, which has no test suite of its own — its correctness is proved only by the pull requests it opens in the repositories that call it.

## 4. Rules this agent must follow

- Read and obey **CONSTITUTION.md** (philosophy + clean-code policy). On conflict, it
  wins over this file.
- Follow **GOVERNANCE.md** for the repo map, documentation policy, and archiving rules.
- Keep `README.md` the single source of truth; `index.html` mirrors it.
- Keep local and remote in harmony: after a sanctioned change, commit and push so the
  GitHub copy matches the working copy.
- Sign in and sign out every landing, with the real clock time.
- **Treat `.github/actions/docs-sync/` as production infrastructure.** A change there
  takes effect across the whole portfolio the next time any caller publishes a release,
  with no staging step and no test that would catch a mistake here. Do not edit it as a
  side effect of another task, and never rewrite git history on this branch — the
  `@master` reference would move under every caller.
- This repository is public and its README is the profile page. Nothing employer-specific
  and nothing private goes in it.

## 5. Ledger (sign-in / sign-out)

## [2026-11-27 05:27 EET] — sami (OpenMausBot), owner-authorised governance landing

STATUS: SIGN-IN (work in progress)

Task: Bring this repository onto the portfolio governance standard, as the owner approved in chat on 2026-11-27 ("bring the remaining eleven onto the same governance standard"). Add the missing root documents, land the shared root-document gate, and give the repository CI of its own.

Touched: Will add `AGENTS.md`, `CHANGELOG.md`, `CONSTITUTION.md`, `GOVERNANCE.md`, `LICENSE`, `scripts/check_root_docs.py` and `.github/workflows/ci.yml`. Nothing is moved, renamed or deleted, and `.github/actions/docs-sync/` is deliberately not touched.

Why: This repository held the profile README, the portfolio index, and the shared docs-sync action that every other repository calls — but no charter, no constitution, no written policy, no changelog, no licence file and no CI of its own. It is infrastructure; it should carry the same standard as what depends on it.

Verification: Planned — `python3 scripts/check_root_docs.py` and `--self-test` locally, then the `ci` and `secret-scan` workflows on the landing commit.

Left undone: Nothing at sign-in.

Sensitive: `git push origin master` (owner's instruction in chat, 2026-11-27). No force push, no history rewrite — other repositories pin the shared action to this branch. No secrets.

## [2026-11-27 05:29 EET] — sami (OpenMausBot), owner-authorised governance landing

STATUS: SIGN-OUT (landing complete)

Task: Bring this repository onto the portfolio governance standard, as the owner approved in chat on 2026-11-27. Done.

Touched: `AGENTS.md`, `CHANGELOG.md`, `CONSTITUTION.md`, `GOVERNANCE.md`, `LICENSE` (all new); `scripts/check_root_docs.py` (new, md5 `35fc37ab16ff4461a33d4e2dcaedb7bf`, byte-identical to the copy in Assay, createlee, Helix-Solutions, Helix-Matrix, Helix-Codex and the six repositories landed earlier today); `.github/workflows/ci.yml` (new, one `governance` job). Nothing moved, renamed or deleted. `.github/actions/docs-sync/` (`action.yml`, `render_docs.py`) was deliberately not touched: fourteen-plus repositories pin it as `Hatemshalaby15071979/Hatemshalaby15071979/.github/actions/docs-sync@master`, so a change there lands everywhere at the next release with no staging step.

Why: This repository held the profile README, the portfolio index and the shared docs-sync action every other repository calls — but no charter, no constitution, no written policy, no changelog, no licence file and no CI of its own. It is infrastructure; it now carries the same standard as what depends on it. `GOVERNANCE.md` section 1 records the shared-action hazard in writing for the first time.

Verification: `python3 scripts/check_root_docs.py` → "OK -- Hatemshalaby15071979/ holds only the GOVERNANCE.md section 2 set" (7 table rows, 7 allowed root documents; `_docs_profile.json` and `index.html` are not `.md`/`.txt`, so the gate correctly ignores them). `--self-test` → 7/7 cases behaved: a planted `STRAY-NOTE.md` and a planted `NOTES.txt` each stop the gate, a missing required document stops it, a package manifest at the root is acknowledged as a non-document, a stray under `docs/` is ignored, and a section 2 with no parsable table fails closed. `.github/workflows/ci.yml` parses as valid YAML with one job `governance` on `ubuntu-latest`, two steps. `README.md` already carries the Helix Solutions logo and needed no change. Note for the next agent: the default branch here is `master`, not `main` — that is load-bearing, because the shared action is referenced with `@master`.

Left undone: Nothing failing. CI on this landing and the sign-out commit is the record of the same steps on a clean runner.

Sensitive: `git push origin master` (owner's instruction in chat, 2026-11-27). No force push, no history rewrite — other repositories pin the shared action to this branch. No secrets.

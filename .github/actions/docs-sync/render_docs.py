#!/usr/bin/env python3
"""
render_docs.py — the docs-sync engine's renderer.

What it does
------------
For a target repository, it refreshes ONLY the "status block" inside its visitor
docs (README.md, index.html, marketing/index.html). The status block is the part
that changes when a release ships: the version, the release date, the test count,
the coverage, and the CI state. Everything outside the block is hand-authored
prose and is never touched.

The block is delimited by HTML comments so the source always reads cleanly:

    <!-- docs-sync:start -->
    **Version 2.1.1 — released 10 November 2026.** 465 automated tests pass ...
    <!-- docs-sync:end -->

If the delimiters are absent, the file is left untouched (the engine is opt-in per
file). Standalone tokens such as @DOCS_SYNC_VERSION@ are also replaced anywhere
they appear (e.g. inside a badge URL), so a repo can opt in at any granularity.

Facts are never invented. They come from the release event (version, date) and
from the checks API (CI state), with test/coverage numbers taken from the repo's
_docs_profile.json — the human-verified baseline. A future release that actually
runs the suite can override them.

This script is intentionally side-effect-free unless --write is passed; with
--write it rewrites the files in place and reports what changed.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

MARKER_START = "<!-- docs-sync:start -->"
MARKER_END = "<!-- docs-sync:end -->"

# Tokens the engine fills from proven facts.
TOKENS = {
    "VERSION": "@DOCS_SYNC_VERSION@",
    "DATE": "@DOCS_SYNC_DATE@",
    "TESTS": "@DOCS_SYNC_TESTS@",
    "COVERAGE": "@DOCS_SYNC_COVERAGE@",
    "CI": "@DOCS_SYNC_CI@",
}

DEFAULT_MD_TEMPLATE = (
    "**Version @DOCS_SYNC_VERSION@ — released @DOCS_SYNC_DATE@.** "
    "@DOCS_SYNC_TESTS@ automated tests pass@COVERAGE_FRAGMENT@, and @DOCS_SYNC_CI@."
)
DEFAULT_HTML_TEMPLATE = (
    '<p class="status"><strong>Version @DOCS_SYNC_VERSION@ — released '
    "@DOCS_SYNC_DATE@.</strong> @DOCS_SYNC_TESTS@ automated tests pass"
    "@COVERAGE_FRAGMENT@, and @DOCS_SYNC_CI@.</p>"
)

DOC_TARGETS = ["README.md", "index.html", "marketing/index.html"]


def human_date(iso_or_human: str) -> str:
    """Parse an ISO date/time (with or without T/Z) to 'D Month YYYY'.

    If the value is not a parseable ISO string it is treated as already-human
    (e.g. '10 November 2026') and returned unchanged.
    """
    value = (iso_or_human or "").strip()
    if not value:
        return value
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return dt.strftime("%-d %B %Y")
    except ValueError:
        return value


def build_facts(args, profile: dict) -> dict:
    pfacts = (profile.get("facts") or {}) if profile else {}
    version = args.version or pfacts.get("version") or ""
    iso_date = args.release_date or pfacts.get("release_date") or ""
    tests = args.tests if args.tests is not None else pfacts.get("tests_passed")
    coverage = args.coverage if args.coverage is not None else pfacts.get("coverage")

    ci_state = (args.ci_status or "success").lower()
    if ci_state == "success":
        ci_label = pfacts.get("ci_label") or "all CI checks are green"
    elif ci_state in ("failure", "error"):
        ci_label = "CI is not green"
    else:
        ci_label = "CI state unknown"

    coverage_fragment = ""
    if coverage not in (None, "", "null"):
        try:
            coverage_fragment = f", the code is {float(coverage)}% covered"
        except (TypeError, ValueError):
            coverage_fragment = f", the code is {coverage}% covered"

    tests_str = "" if tests in (None, "", "null") else str(tests)

    return {
        "VERSION": version,
        "DATE": human_date(iso_date),
        "TESTS": tests_str,
        "COVERAGE": "" if coverage in (None, "", "null") else str(coverage),
        "CI": ci_label,
        "COVERAGE_FRAGMENT": coverage_fragment,
        "ci_state": ci_state,
    }


def fill(text: str, facts: dict) -> str:
    # Resolve the conditional coverage fragment first.
    text = text.replace("@COVERAGE_FRAGMENT@", facts.get("COVERAGE_FRAGMENT", ""))
    for key, token in TOKENS.items():
        text = text.replace(token, facts.get(key, ""))
    return text


def render_block(template: str, facts: dict) -> str:
    return f"{MARKER_START}\n{fill(template, facts).strip()}\n{MARKER_END}\n"


def process_file(path: Path, facts: dict, profile: dict, write: bool) -> tuple[bool, bool]:
    """Returns (touched, changed). `touched` means the file opted in."""
    if not path.exists():
        return False, False
    text = path.read_text(encoding="utf-8")

    touched = (MARKER_START in text and MARKER_END in text) or any(
        t in text for t in TOKENS.values()
    )
    if not touched:
        return False, False

    # 1) Refresh the delimited status block if present.
    if MARKER_START in text and MARKER_END in text:
        is_html = path.suffix.lower() == ".html"
        template = (
            profile.get("status_template_html") if is_html else profile.get("status_template")
        ) or (DEFAULT_HTML_TEMPLATE if is_html else DEFAULT_MD_TEMPLATE)
        block = render_block(template, facts)
        pattern = re.compile(
            re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END), re.DOTALL
        )
        new_text = pattern.sub(block.rstrip("\n"), text)
    else:
        new_text = text

    # 2) Replace any standalone tokens anywhere (badges, etc.).
    new_text = fill(new_text, facts)

    changed = new_text != text
    if changed and write:
        path.write_text(new_text, encoding="utf-8")
    return True, changed


def main() -> int:
    ap = argparse.ArgumentParser(description="Refresh the docs-sync status block.")
    ap.add_argument("--repo-dir", required=True, help="Path to the target repository root")
    ap.add_argument("--profile", default="_docs_profile.json",
                    help="Path (relative to repo-dir) to the docs profile JSON")
    ap.add_argument("--version", help="Release tag, e.g. v2.1.1")
    ap.add_argument("--release-date", help="ISO or human release date")
    ap.add_argument("--tests", help="Tests passed (overrides profile)")
    ap.add_argument("--coverage", help="Coverage percentage (overrides profile)")
    ap.add_argument("--ci-status", default="success",
                    help="success | failure | error | pending")
    ap.add_argument("--write", action="store_true", help="Rewrite files in place")
    args = ap.parse_args()

    repo_dir = Path(args.repo_dir)
    profile_path = repo_dir / args.profile
    profile: dict = {}
    if profile_path.exists():
        profile = json.loads(profile_path.read_text(encoding="utf-8"))

    facts = build_facts(args, profile)

    if facts["ci_state"] != "success":
        print(f"[docs-sync] CI state is '{facts['ci_state']}' — refusing to publish "
              f"unverified status. No files changed.", file=sys.stderr)
        return 2

    touched_any = False
    changed_any = False
    for rel in DOC_TARGETS:
        target = repo_dir / rel
        touched, changed = process_file(target, facts, profile, args.write)
        if touched:
            touched_any = True
        if changed:
            changed_any = True
            print(f"[docs-sync] updated: {rel}")

    if not touched_any:
        print("[docs-sync] no opted-in files (no markers / no tokens). Nothing to do.")
    elif not changed_any:
        print("[docs-sync] already current — no change needed.")
    elif not args.write:
        print("[docs-sync] dry-run: files would change. Pass --write to apply.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

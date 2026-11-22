#!/usr/bin/env python3
"""Repository linter for managed instruction files and pull request metadata."""

from __future__ import annotations

import argparse
import os
import pathlib
import re
import subprocess
import sys

import build

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
MANAGED_PATH_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*/[a-z0-9]+(?:-[a-z0-9]+)*\.md$")

ROOT_ALLOWED_FILES = frozenset(
    {".gitattributes", ".gitignore", "AGENTS.md", "CLAUDE.md", "LICENSE", "README.md"}
)
# .claude holds only a symlink to .agents/skills, which is linted at its real path.
FRAGMENT_PATH_RE = re.compile(r"^shared/[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
SOURCE_PATH_RE = re.compile(r"^src/[a-z0-9]+(?:-[a-z0-9]+)*/[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
UNLINTED_TOP_DIRS = frozenset({".claude", ".github", "scripts"})

EM_DASH_RE = re.compile(r"[\u2014\u2015\u2e3a]")
CURLY_QUOTE_RE = re.compile(r"[\u2018\u2019\u201c\u201d]")
CIRCLED_NUM_RE = re.compile(
    r"[\u2460-\u2473\u24ea\u24f5-\u24fe\u2776-\u2793\u3251-\u325f\u32b1-\u32bf]"
)
INLINE_CODE_RE = re.compile(r"`[^`]*`")
NON_NAME_MID_DOT_RE = re.compile(
    r"(?<![\u4e00-\u9fff])[\u00b7\u30fb]|[\u00b7\u30fb](?![\u4e00-\u9fff])"
)
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")


def lint_markdown_file(path: pathlib.Path, rel_path: str) -> tuple[list[str], int, int]:
    errors: list[str] = []
    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()
    in_fence = False

    for line_num, raw_line in enumerate(lines, start=1):
        stripped = raw_line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        # Inline code is exempt, so a rule can name a forbidden character in backticks.
        without_code = INLINE_CODE_RE.sub("", raw_line)

        if EM_DASH_RE.search(without_code):
            errors.append(f"{rel_path}:{line_num}: forbidden em-dash")
        if CURLY_QUOTE_RE.search(without_code):
            errors.append(f"{rel_path}:{line_num}: forbidden curly quote")
        if CIRCLED_NUM_RE.search(without_code):
            errors.append(f"{rel_path}:{line_num}: forbidden circled number")

        is_table_row = (
            stripped.startswith("|") and stripped.endswith("|") and len(stripped) > 1
        )
        if not is_table_row and "|" in without_code:
            errors.append(f"{rel_path}:{line_num}: forbidden inline vertical bar '|'")
        if NON_NAME_MID_DOT_RE.search(without_code):
            errors.append(f"{rel_path}:{line_num}: forbidden inline mid dot")

    return errors, len(content), len(lines)


def list_repo_files() -> list[str]:
    """Return tracked and untracked-but-not-ignored paths, so local clutter is skipped."""
    output = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    paths = sorted({p for p in output.split("\0") if p})
    return [p for p in paths if (REPO_ROOT / p).is_file() or (REPO_ROOT / p).is_symlink()]


def collect_files() -> tuple[list[tuple[pathlib.Path, str]], list[tuple[pathlib.Path, str]], list[str]]:
    """Split repository files into managed instruction files and other linted docs."""
    managed_files: list[tuple[pathlib.Path, str]] = []
    doc_files: list[tuple[pathlib.Path, str]] = []
    errors: list[str] = []

    for rel_posix in list_repo_files():
        full_path = REPO_ROOT / rel_posix
        parts = pathlib.PurePosixPath(rel_posix).parts

        if len(parts) == 1:
            if rel_posix not in ROOT_ALLOWED_FILES:
                errors.append(
                    f"{rel_posix}: unexpected root file (allowed: {', '.join(sorted(ROOT_ALLOWED_FILES))})"
                )
            elif rel_posix.endswith(".md"):
                doc_files.append((full_path, rel_posix))
            continue

        if parts[0] in UNLINTED_TOP_DIRS:
            continue
        if parts[0] == ".agents":
            if rel_posix.endswith(".md"):
                doc_files.append((full_path, rel_posix))
            continue

        if parts[0] == "shared":
            if FRAGMENT_PATH_RE.match(rel_posix):
                doc_files.append((full_path, rel_posix))
            else:
                errors.append(f"{rel_posix}: path must match shared/<fragment-name>.md in lowercase kebab-case")
            continue
        if parts[0] == "src":
            if SOURCE_PATH_RE.match(rel_posix):
                doc_files.append((full_path, rel_posix))
            else:
                errors.append(
                    f"{rel_posix}: path must match src/<client>/<model-slug>.md in lowercase kebab-case"
                )
            continue

        if not MANAGED_PATH_RE.match(rel_posix):
            errors.append(
                f"{rel_posix}: path must match <client>/<model-slug>.md in lowercase kebab-case"
            )
            continue
        managed_files.append((full_path, rel_posix))

    return managed_files, doc_files, errors


def lint_pr_title(title: str) -> list[str]:
    errors: list[str] = []
    if not title or not title.strip():
        errors.append("PR title: must not be empty")
        return errors
    if title != title.strip():
        errors.append("PR title: must not have leading or trailing whitespace")
    if CJK_RE.search(title):
        errors.append("PR title: must be written in English (contains CJK characters)")
    if (
        EM_DASH_RE.search(title)
        or CURLY_QUOTE_RE.search(title)
        or CIRCLED_NUM_RE.search(title)
    ):
        errors.append(
            "PR title: contains forbidden punctuation (em-dash, curly quote, or circled number)"
        )
    return errors


def write_step_summary(stats: list[tuple[str, int, int]]) -> None:
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path or not stats:
        return
    rows = [
        "### Instruction File Metrics",
        "",
        "| File | Characters | Lines |",
        "| :--- | ---: | ---: |",
    ]
    for rel_path, char_count, line_count in stats:
        rows.append(f"| `{rel_path}` | {char_count} | {line_count} |")
    rows.append("")
    with open(summary_path, "a", encoding="utf-8") as handle:
        handle.write("\n".join(rows))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pr-title", default=None, help="Validate a PR title string.")
    args = parser.parse_args()

    managed_files, doc_files, errors = collect_files()
    stats: list[tuple[str, int, int]] = []

    for full_path, rel_path in managed_files:
        file_errors, char_count, line_count = lint_markdown_file(full_path, rel_path)
        errors.extend(file_errors)
        stats.append((rel_path, char_count, line_count))

    for full_path, rel_path in doc_files:
        file_errors, _, _ = lint_markdown_file(full_path, rel_path)
        errors.extend(file_errors)

    outputs, build_errors = build.build_all()
    errors.extend(build_errors)
    errors.extend(build.check_outputs(outputs))
    for _, rel_path in managed_files:
        if rel_path not in outputs:
            errors.append(
                f"{rel_path}: no source at src/{rel_path}; instruction files are generated, edit src/ instead"
            )

    pr_title = (
        args.pr_title if args.pr_title is not None else os.environ.get("PR_TITLE")
    )
    if args.pr_title is not None or os.environ.get("GITHUB_EVENT_NAME") == "pull_request":
        errors.extend(lint_pr_title(pr_title or ""))

    for rel_path, char_count, line_count in stats:
        print(f"OK  {rel_path} ({char_count} chars, {line_count} lines)")

    write_step_summary(stats)

    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

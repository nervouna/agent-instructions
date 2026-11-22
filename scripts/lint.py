#!/usr/bin/env python3
"""Repository linter for managed instruction files and pull request metadata."""

from __future__ import annotations

import argparse
import os
import pathlib
import re
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
MANAGED_PATH_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*/[a-z0-9]+(?:-[a-z0-9]+)*\.md$")

ALLOWED_DECLARATIONS = (
    "instead of \u201c\u201d",
    "(\u2014 and \u2014\u2014)",
    "(\u00b7)",
    "(|)",
)

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


def strip_allowed_declarations(line: str) -> str:
    cleaned = line
    for phrase in ALLOWED_DECLARATIONS:
        cleaned = cleaned.replace(phrase, "")
    return cleaned


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

        cleaned = strip_allowed_declarations(raw_line)
        without_code = INLINE_CODE_RE.sub("", cleaned)

        if EM_DASH_RE.search(cleaned):
            errors.append(f"{rel_path}:{line_num}: forbidden em-dash")
        if CURLY_QUOTE_RE.search(cleaned):
            errors.append(f"{rel_path}:{line_num}: forbidden curly quote")
        if CIRCLED_NUM_RE.search(cleaned):
            errors.append(f"{rel_path}:{line_num}: forbidden circled number")

        is_table_row = (
            stripped.startswith("|") and stripped.endswith("|") and len(stripped) > 1
        )
        if not is_table_row and "|" in without_code:
            errors.append(f"{rel_path}:{line_num}: forbidden inline vertical bar '|'")
        if NON_NAME_MID_DOT_RE.search(without_code):
            errors.append(f"{rel_path}:{line_num}: forbidden inline mid dot")

    return errors, len(content), len(lines)


def collect_files() -> tuple[list[tuple[pathlib.Path, str]], list[tuple[pathlib.Path, str]], list[str]]:
    managed_files: list[tuple[pathlib.Path, str]] = []
    skill_files: list[tuple[pathlib.Path, str]] = []
    errors: list[str] = []

    for root, dirs, files in os.walk(REPO_ROOT):
        rel_root = pathlib.Path(root).relative_to(REPO_ROOT)
        top_part = rel_root.parts[0] if rel_root.parts else ""

        if not rel_root.parts:
            dirs[:] = sorted(d for d in dirs if d != ".git")
        else:
            dirs.sort()

        for filename in sorted(files):
            full_path = pathlib.Path(root) / filename
            rel_posix = full_path.relative_to(REPO_ROOT).as_posix()

            if top_part in {".github", "scripts"}:
                continue
            if top_part == ".agents":
                if filename.endswith(".md"):
                    skill_files.append((full_path, rel_posix))
                continue

            if not MANAGED_PATH_RE.match(rel_posix):
                errors.append(
                    f"{rel_posix}: path must match <client>/<model-slug>.md in lowercase kebab-case"
                )
                continue
            managed_files.append((full_path, rel_posix))

    return managed_files, skill_files, errors


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

    managed_files, skill_files, errors = collect_files()
    stats: list[tuple[str, int, int]] = []

    for full_path, rel_path in managed_files:
        file_errors, char_count, line_count = lint_markdown_file(full_path, rel_path)
        errors.extend(file_errors)
        stats.append((rel_path, char_count, line_count))

    for full_path, rel_path in skill_files:
        file_errors, _, _ = lint_markdown_file(full_path, rel_path)
        errors.extend(file_errors)

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

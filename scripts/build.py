#!/usr/bin/env python3

from __future__ import annotations

import argparse
import pathlib
import re
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "src"
SHARED_DIR = REPO_ROOT / "shared"
INCLUDE_RE = re.compile(r"^\{\{\s*([a-z0-9]+(?:-[a-z0-9]+)*)\s*\}\}$")


def load_fragments() -> dict[str, str]:
    return {
        path.stem: path.read_text(encoding="utf-8").rstrip("\n")
        for path in sorted(SHARED_DIR.glob("*.md"))
    }


def render(source: str, fragments: dict[str, str], rel_path: str) -> tuple[str, set[str], list[str]]:
    lines: list[str] = []
    used: set[str] = set()
    errors: list[str] = []
    for line_num, line in enumerate(source.splitlines(), start=1):
        match = INCLUDE_RE.match(line)
        if not match:
            lines.append(line)
            continue
        name = match.group(1)
        if name not in fragments:
            errors.append(f"{rel_path}:{line_num}: unknown fragment '{name}' (no shared/{name}.md)")
            continue
        used.add(name)
        lines.append(fragments[name])
    return "\n".join(lines) + "\n", used, errors


def build_all() -> tuple[dict[str, str], list[str]]:
    fragments = load_fragments()
    outputs: dict[str, str] = {}
    errors: list[str] = []
    used: set[str] = set()

    for source_path in sorted(SRC_DIR.rglob("*.md")):
        rel_source = source_path.relative_to(REPO_ROOT).as_posix()
        rel_output = source_path.relative_to(SRC_DIR).as_posix()
        text, file_used, file_errors = render(
            source_path.read_text(encoding="utf-8"), fragments, rel_source
        )
        outputs[rel_output] = text
        used |= file_used
        errors.extend(file_errors)

    for name in sorted(set(fragments) - used):
        errors.append(f"shared/{name}.md: not included by any source")

    return outputs, errors


def check_outputs(outputs: dict[str, str]) -> list[str]:
    errors: list[str] = []
    for rel_output, text in outputs.items():
        path = REPO_ROOT / rel_output
        if not path.is_file():
            errors.append(f"{rel_output}: missing; run python3 scripts/build.py")
        elif path.read_text(encoding="utf-8") != text:
            errors.append(f"{rel_output}: out of date with src/{rel_output}; run python3 scripts/build.py")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Build instruction files from src/ sources and shared/ fragments.")
    parser.add_argument("--check", action="store_true", help="Verify outputs instead of writing them.")
    args = parser.parse_args()

    outputs, errors = build_all()
    if args.check:
        errors.extend(check_outputs(outputs))
    elif not errors:
        for rel_output, text in outputs.items():
            path = REPO_ROOT / rel_output
            path.parent.mkdir(parents=True, exist_ok=True)
            changed = not path.is_file() or path.read_text(encoding="utf-8") != text
            if changed:
                path.write_text(text, encoding="utf-8")
            print(f"{'WROTE' if changed else 'SAME '} {rel_output}")

    for err in errors:
        print(f"ERROR: {err}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

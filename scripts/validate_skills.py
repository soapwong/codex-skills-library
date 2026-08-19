#!/usr/bin/env python3
"""Validate every Codex skill in this repository."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", re.DOTALL)
ALLOWED_FRONTMATTER = {
    "name",
    "description",
    "license",
    "allowed-tools",
    "metadata",
}


def load_yaml(path: Path) -> object:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise ValueError(f"cannot parse YAML: {exc}") from exc


def validate_openai_yaml(path: Path, skill_name: str) -> list[str]:
    errors: list[str] = []
    try:
        data = load_yaml(path)
    except ValueError as exc:
        return [str(exc)]

    if not isinstance(data, dict):
        return ["top level must be a mapping"]

    interface = data.get("interface")
    if interface is None:
        return errors
    if not isinstance(interface, dict):
        return ["interface must be a mapping"]

    short_description = interface.get("short_description")
    if short_description is not None:
        if not isinstance(short_description, str):
            errors.append("interface.short_description must be a string")
        elif not 25 <= len(short_description) <= 64:
            errors.append("interface.short_description must contain 25-64 characters")

    default_prompt = interface.get("default_prompt")
    if default_prompt is not None:
        if not isinstance(default_prompt, str):
            errors.append("interface.default_prompt must be a string")
        elif f"${skill_name}" not in default_prompt:
            errors.append(f"interface.default_prompt must mention ${skill_name}")

    return errors


def validate_skill(skill_file: Path) -> tuple[str | None, list[str]]:
    errors: list[str] = []
    relative = skill_file.relative_to(SKILLS_ROOT)
    if len(relative.parts) != 3:
        return None, [
            "SKILL.md must be located at skills/<category>/<skill-name>/SKILL.md"
        ]

    category, folder_name, _ = relative.parts
    if not NAME_RE.fullmatch(category):
        errors.append(f"invalid category name: {category}")
    if not NAME_RE.fullmatch(folder_name):
        errors.append(f"invalid skill folder name: {folder_name}")

    try:
        content = skill_file.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return None, [f"cannot read UTF-8 text: {exc}"]

    match = FRONTMATTER_RE.match(content)
    if not match:
        return None, errors + ["missing or invalid YAML frontmatter"]

    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return None, errors + [f"cannot parse frontmatter: {exc}"]

    if not isinstance(frontmatter, dict):
        return None, errors + ["frontmatter must be a mapping"]

    unexpected = set(frontmatter) - ALLOWED_FRONTMATTER
    if unexpected:
        errors.append(f"unexpected frontmatter keys: {', '.join(sorted(unexpected))}")

    name = frontmatter.get("name")
    if not isinstance(name, str) or not name:
        errors.append("frontmatter.name must be a non-empty string")
        name = None
    else:
        if not NAME_RE.fullmatch(name) or len(name) > 64:
            errors.append("frontmatter.name must be kebab-case and at most 64 characters")
        if name != folder_name:
            errors.append(
                f"frontmatter.name '{name}' does not match folder '{folder_name}'"
            )

    description = frontmatter.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append("frontmatter.description must be a non-empty string")
    elif len(description) > 1024 or "<" in description or ">" in description:
        errors.append("frontmatter.description is invalid or longer than 1024 characters")

    body = content[match.end() :]
    if re.search(r"(?m)^\s*\[TODO:[^\n]*\]\s*$", body):
        errors.append("unfinished TODO placeholder found")

    openai_yaml = skill_file.parent / "agents" / "openai.yaml"
    if openai_yaml.exists() and name:
        errors.extend(
            f"agents/openai.yaml: {error}"
            for error in validate_openai_yaml(openai_yaml, name)
        )

    return name, errors


def main() -> int:
    skill_files = sorted(SKILLS_ROOT.rglob("SKILL.md"))
    if not skill_files:
        print("ERROR: no skills found", file=sys.stderr)
        return 1

    failures: list[str] = []
    names: dict[str, Path] = {}

    for skill_file in skill_files:
        name, errors = validate_skill(skill_file)
        display_path = skill_file.relative_to(ROOT)
        for error in errors:
            failures.append(f"{display_path}: {error}")

        if name:
            if name in names:
                failures.append(
                    f"{display_path}: duplicate skill name also used by "
                    f"{names[name].relative_to(ROOT)}"
                )
            else:
                names[name] = skill_file

    if failures:
        for failure in failures:
            print(f"ERROR: {failure}", file=sys.stderr)
        return 1

    print(f"Validated {len(skill_files)} skill(s): {', '.join(sorted(names))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

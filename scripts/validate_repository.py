#!/usr/bin/env python3
"""Validate the GitHub-backed Finn Loop artifact repository."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path


IGNORED_DIRECTORIES = {
    ".git",
    ".netlify",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
    "node_modules",
}
REQUIRED_DIRECTORIES = {"assets", "campaigns", "research", "reviews", "runs"}
REQUIRED_LABEL_FIELDS = {
    "approval_label",
    "blocked_label",
    "in_progress_label",
    "review_label",
    "spec_drafted_label",
    "approved_label",
    "changes_requested_label",
    "human_review_label",
}
FORBIDDEN_NAMES = {
    ".env",
    "credentials.json",
    "id_rsa",
    "id_ed25519",
}
FORBIDDEN_SUFFIXES = {".key", ".p12", ".pfx", ".pem"}
MAX_FILE_BYTES = 95 * 1024 * 1024
MAX_SECRET_SCAN_BYTES = 5 * 1024 * 1024
SECRET_PATTERNS = {
    "private_key": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github_token": re.compile(rb"(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})"),
    "openai_key": re.compile(rb"sk-[A-Za-z0-9_-]{20,}"),
    "google_key": re.compile(rb"AIza[0-9A-Za-z_-]{20,}"),
    "slack_token": re.compile(rb"xox[baprs]-[0-9A-Za-z-]{10,}"),
}


def iter_files(root: Path):
    for current, directories, filenames in os.walk(root, followlinks=False):
        directories[:] = sorted(
            name for name in directories if name not in IGNORED_DIRECTORIES
        )
        current_path = Path(current)
        for filename in sorted(filenames):
            yield current_path / filename


def relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()
    errors: list[str] = []

    missing_directories = sorted(
        name for name in REQUIRED_DIRECTORIES if not (root / name).is_dir()
    )
    if missing_directories:
        errors.append("missing_directories=" + ",".join(missing_directories))

    config_path = root / ".finn-loop.json"
    config: dict[str, object] = {}
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"invalid_finn_config={error}")

    if config:
        if config.get("schema_version") != 1:
            errors.append("finn_config_schema_version_must_equal_1")
        if config.get("tracker") != "github":
            errors.append("finn_config_tracker_must_equal_github")
        repository = config.get("repository")
        if not isinstance(repository, str) or not re.fullmatch(
            r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository
        ):
            errors.append("finn_config_repository_invalid")
        for field in sorted(REQUIRED_LABEL_FIELDS):
            value = config.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"finn_config_missing_{field}")
        if config.get("human_merge_only") is not True:
            errors.append("finn_config_human_merge_only_must_be_true")

    file_count = 0
    json_count = 0
    for path in iter_files(root):
        file_count += 1
        rel = relative(path, root)
        if path.is_symlink():
            errors.append(f"symlink_not_allowed={rel}")
            continue
        try:
            size = path.stat().st_size
        except OSError as error:
            errors.append(f"unreadable_file={rel}:{error}")
            continue
        if size > MAX_FILE_BYTES:
            errors.append(f"oversized_file={rel}:{size}")
        if path.name in FORBIDDEN_NAMES or path.suffix.lower() in FORBIDDEN_SUFFIXES:
            errors.append(f"credential_filename={rel}")

        if path.suffix.lower() == ".json":
            json_count += 1
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
                errors.append(f"invalid_json={rel}:{error}")

        if size <= MAX_SECRET_SCAN_BYTES:
            try:
                content = path.read_bytes()
            except OSError:
                continue
            if b"\x00" not in content[:8192]:
                for name, pattern in SECRET_PATTERNS.items():
                    if pattern.search(content):
                        errors.append(f"possible_secret_{name}={rel}")

    if errors:
        for error in errors:
            print("ERROR " + error)
        print(f"VALIDATION_FAIL errors={len(errors)} files={file_count} json={json_count}")
        return 1

    print(f"VALIDATION_PASS files={file_count} json={json_count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

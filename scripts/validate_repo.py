
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List


TOOL_DIRS = ("molsysmt", "molsysviewer", "molsys-ai")
PAPER_DIR_RE = re.compile(r"^\d{4}-[a-z0-9][a-z0-9-]*$")  # e.g. 2026-molsysmt-foundation


@dataclass
class Err:
    msg: str


def fail(errors: List[Err]) -> int:
    for e in errors:
        print(f"ERROR: {e.msg}")
    return 1


def warn(msg: str) -> None:
    print(f"WARNING: {msg}")


def check_file(p: Path, errors: List[Err]) -> None:
    if not p.exists():
        errors.append(Err(f"Missing required file: {p}"))


def check_dir(p: Path, errors: List[Err]) -> None:
    if not p.exists() or not p.is_dir():
        errors.append(Err(f"Missing required directory: {p}"))


def validate_paper_dir(paper_dir: Path, errors: List[Err], strict: bool) -> None:
    # Required
    for rel in ("README.md", "manuscript", "figures", "bibliography"):
        target = paper_dir / rel
        if rel.endswith(".md"):
            if not target.exists():
                errors.append(Err(f"{paper_dir}: missing {rel}"))
        else:
            if not target.exists() or not target.is_dir():
                errors.append(Err(f"{paper_dir}: missing directory {rel}/"))

    # Optional
    artifacts = paper_dir / "artifacts"
    if strict and (not artifacts.exists() or not artifacts.is_dir()):
        warn(f"{paper_dir}: artifacts/ is recommended (strict mode expects it).")


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate molsyssuite-papers repository structure.")
    ap.add_argument("--repo-root", default=".", help="Repository root (default: .)")
    ap.add_argument("--strict", action="store_true", help="Stricter checks (recommended for CI).")
    args = ap.parse_args()

    root = Path(args.repo_root).resolve()
    errors: List[Err] = []

    # Top-level required files/dirs
    check_file(root / "README.md", errors)
    check_file(root / "CONTRIBUTING.md", errors)
    check_dir(root / "templates", errors)
    check_file(root / "templates" / "paper-README.md", errors)
    check_file(root / "templates" / "structure.txt", errors)

    # Tool directories exist
    for t in TOOL_DIRS:
        check_dir(root / t, errors)

    # Validate paper directories
    for tool in TOOL_DIRS:
        tool_dir = root / tool
        if not tool_dir.exists():
            continue

        for child in sorted(tool_dir.iterdir()):
            if not child.is_dir():
                continue
            name = child.name
            if name.startswith("."):
                continue

            if not PAPER_DIR_RE.match(name):
                warn(f"{child}: directory name does not match 'YYYY-slug' (e.g. 2026-molsysmt-foundation).")
                if args.strict:
                    errors.append(Err(f"{child}: invalid paper directory name"))
                    continue

            validate_paper_dir(child, errors, args.strict)

    if errors:
        return fail(errors)

    print("OK: repository structure looks good.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

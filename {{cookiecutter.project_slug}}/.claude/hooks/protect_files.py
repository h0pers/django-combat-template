import json
import re
import subprocess
import sys
from pathlib import Path

SECRET_FILES = re.compile(r"^(\.env(\..+)?|walg\.env)$")
MIGRATION = re.compile(r"/migrations/\d{4}_\w+\.py$")
LOCKFILES = {
    "uv.lock": "Change dependencies with `uv add <pkg>` or `uv remove <pkg>`.",
    "package-lock.json": "Change dependencies with `npm install <pkg>` in frontend/.",
}


def is_tracked(path: Path) -> bool:
    try:
        result = subprocess.run(
            ["git", "ls-files", "--error-unmatch", path.name],
            cwd=path.parent,
            capture_output=True,
        )
    except OSError:
        return True
    return result.returncode == 0


def reason_to_block(path: Path) -> str | None:
    name = path.name

    if SECRET_FILES.match(name) and not name.endswith(".example"):
        return (
            f"{name} holds secrets and is edited by people only. "
            "Document new variables in .env.example instead."
        )

    if name in LOCKFILES:
        return f"{name} is generated. {LOCKFILES[name]}"

    if MIGRATION.search(path.as_posix()) and path.exists() and is_tracked(path):
        return (
            f"{name} is a committed migration and must not change. "
            "Change the model and run `make makemigrations ARGS=<app>` instead."
        )

    return None


def main() -> int:
    payload = json.load(sys.stdin)
    file_path = payload.get("tool_input", {}).get("file_path")
    if not file_path:
        return 0

    reason = reason_to_block(Path(file_path))
    if reason:
        sys.stderr.write(f"Blocked: {reason}\n")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())

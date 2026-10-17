import json
import os
import shutil
import subprocess
import sys


def ruff(*args: str, cwd: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["uv", "run", "--quiet", "ruff", *args, "--force-exclude"],
        cwd=cwd,
        capture_output=True,
        text=True,
    )


def main() -> int:
    payload = json.load(sys.stdin)
    file_path = payload.get("tool_input", {}).get("file_path", "")
    if not file_path.endswith(".py") or shutil.which("uv") is None:
        return 0

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", payload.get("cwd", "."))
    check = ruff(
        "check",
        "--fix",
        "--output-format",
        "concise",
        file_path,
        cwd=project_dir,
    )
    ruff("format", file_path, cwd=project_dir)

    if check.returncode != 0:
        sys.stderr.write(
            f"ruff found problems it could not fix:\n{check.stdout}{check.stderr}"
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())

import shutil
import subprocess
from pathlib import Path

USE_DRF = "{{ cookiecutter.use_drf }}" == "y"
USE_WAGTAIL = "{{ cookiecutter.use_wagtail }}" == "y"
USE_VUE = "{{ cookiecutter.use_vue }}" == "y"

REMOVE_PATHS_NO_DRF = [
    "website/website/settings/components/rest_framework.py",
    "website/apps/core/api/schema.py",
    "website/apps/core/api/docstring.py",
    "website/apps/core/api/exception_handler.py",
    "website/apps/core/tests/test_exception_handler.py",
    "website/apps/polls/api",
    "website/apps/polls/tests/test_api.py",
    ".claude/rules/api.md",
    ".claude/skills/add-endpoint",
]

REMOVE_PATHS_NO_DRF_AND_NO_VUE = [
    "website/apps/polls",
]

REMOVE_PATHS_NO_WAGTAIL = [
    "website/apps/cms",
    "website/website/settings/components/wagtail.py",
]

REMOVE_PATHS_NO_VUE = [
    "frontend",
    "website/website/settings/components/vite.py",
    "website/apps/polls/templates",
    "website/apps/polls/views.py",
    "website/apps/polls/urls.py",
    ".claude/rules/frontend.md",
]


def remove_paths(paths: list[str]) -> None:
    for path_str in paths:
        path = Path(path_str)
        if path.is_dir():
            shutil.rmtree(path)
        elif path.is_file():
            path.unlink()


def generate_frontend_lock_file() -> None:
    try:
        subprocess.run(["npm", "install", "--package-lock-only"], cwd="frontend", check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("WARNING: Could not run 'npm install --package-lock-only'. Run it manually in frontend/ directory.")


def generate_lock_file() -> None:
    try:
        subprocess.run(["uv", "lock"], check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("WARNING: Could not run 'uv lock'. Run it manually to generate uv.lock.")


def init_git() -> None:
    try:
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("WARNING: Could not initialize git repository. Run 'git init' manually.")


def main() -> None:
    if not USE_DRF:
        remove_paths(REMOVE_PATHS_NO_DRF)

    if not USE_DRF and not USE_VUE:
        remove_paths(REMOVE_PATHS_NO_DRF_AND_NO_VUE)

    if not USE_WAGTAIL:
        remove_paths(REMOVE_PATHS_NO_WAGTAIL)

    if not USE_VUE:
        remove_paths(REMOVE_PATHS_NO_VUE)

    if USE_VUE:
        generate_frontend_lock_file()

    generate_lock_file()
    init_git()


if __name__ == "__main__":
    main()
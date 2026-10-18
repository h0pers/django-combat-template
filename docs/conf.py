project = "Django Combat"
author = "Dmytro Hryshchenko"
copyright = "2026, Dmytro Hryshchenko"
release = "1.0.0"

extensions = [
    "myst_parser",
    "sphinxcontrib.mermaid",
]

myst_enable_extensions = [
    "colon_fence",
    "deflist",
]
# Render plain ```mermaid fences as diagrams, so the same Markdown works on GitHub
myst_fence_as_directive = ["mermaid"]
myst_heading_anchors = 3

exclude_patterns = ["_build"]

html_theme = "sphinx_rtd_theme"
html_title = "Django Combat"
html_context = {
    "display_github": True,
    "github_user": "h0pers",
    "github_repo": "django-combat-template",
    "github_version": "master",
    "conf_py_path": "/docs/",
}

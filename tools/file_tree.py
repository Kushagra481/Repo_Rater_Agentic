from pathlib import Path

IGNORE = {
    ".git", "__pycache__", "node_modules", "venv", ".venv",
    ".pytest_cache", ".mypy_cache", "build", "dist", ".idea", ".vscode"
}

IMPORTANT_NAMES = [
    "README.md", "requirements.txt", "pyproject.toml", "setup.py",
    "package.json", "LICENSE", "CITATION.cff", ".env.example",
    "Dockerfile", "REPO_LAYOUT.md", "USAGE.md",
    "RECOMMENDED_CODING_STYLE.md"
]


def generate_tree(root: Path, max_depth: int = 4) -> str:
    lines = [root.name + "/"]

    def walk(path: Path, prefix: str = "", depth: int = 0):
        if depth >= max_depth:
            return

        entries = [
            p for p in sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
            if p.name not in IGNORE
        ]

        for i, entry in enumerate(entries):
            connector = "└── " if i == len(entries) - 1 else "├── "
            lines.append(prefix + connector + entry.name)

            if entry.is_dir():
                extension = "    " if i == len(entries) - 1 else "│   "
                walk(entry, prefix + extension, depth + 1)

    walk(root)
    return "\n".join(lines)


def read_file(path: Path, limit: int = 12000) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")[:limit]
    except Exception:
        return ""


def important_files(root: Path) -> dict:
    files = {}

    for name in IMPORTANT_NAMES:
        p = root / name
        if p.exists() and p.is_file():
            files[name] = read_file(p)

    if (root / "tests").exists():
        files["tests/"] = "Tests directory exists."

    if (root / "docs").exists():
        files["docs/"] = "Docs directory exists."

    if (root / "csrc").exists():
        files["csrc/"] = "CUDA/C++ source directory exists."

    if (root / "cula").exists():
        files["cula/"] = "Python package directory exists."

    return files
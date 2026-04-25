from pathlib import Path

IGNORE = {
    ".git", "__pycache__", "node_modules", "venv", ".venv",
    ".pytest_cache", ".mypy_cache", "build", "dist", ".idea", ".vscode"
}

IMPORTANT_FILES = [
    "README.md",
    "requirements.txt",
    "pyproject.toml",
    "setup.py",
    "package.json",
    "LICENSE",
    "CITATION.cff",
    ".env.example",
    "Dockerfile",
    "REPO_LAYOUT.md",
    "USAGE.md",
    "CONTRIBUTING.md",
    "RECOMMENDED_CODING_STYLE.md",
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


def collect_important_files(root: Path) -> dict:
    files = {}

    for name in IMPORTANT_FILES:
        path = root / name
        if path.exists() and path.is_file():
            files[name] = read_file(path)

    for folder in ["tests", "docs", "src", "app", "csrc", "scripts", "examples"]:
        if (root / folder).exists() and (root / folder).is_dir():
            files[f"{folder}/"] = f"{folder} directory exists."

    return files


def count_extensions(root: Path) -> dict:
    counts = {}

    for path in root.rglob("*"):
        if any(part in IGNORE for part in path.parts):
            continue

        if path.is_file():
            suffix = path.suffix.lower() or "[no extension]"
            counts[suffix] = counts.get(suffix, 0) + 1

    return counts


def collect_source_stats(root: Path) -> dict:
    source_extensions = {
        ".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".cpp", ".c",
        ".cu", ".h", ".hpp", ".rs", ".go"
    }

    total_files = 0
    large_files = []
    source_files = []

    for path in root.rglob("*"):
        if any(part in IGNORE for part in path.parts):
            continue

        if path.is_file() and path.suffix.lower() in source_extensions:
            total_files += 1
            source_files.append(str(path.relative_to(root)))

            try:
                lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
                if len(lines) > 500:
                    large_files.append({
                        "file": str(path.relative_to(root)),
                        "lines": len(lines)
                    })
            except Exception:
                pass

    return {
        "total_source_files": total_files,
        "large_files": large_files,
        "sample_source_files": source_files[:30],
    }
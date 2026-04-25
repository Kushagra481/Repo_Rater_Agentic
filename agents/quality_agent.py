from pathlib import Path


def quality_agent(state):
    repo_path = Path(state.get("repo_path", ""))
    files = state.get("important_files", {})

    checks = {
        "README exists": "README.md" in files,
        "Python packaging exists": "pyproject.toml" in files or "setup.py" in files,
        "Tests exist": "tests/" in files,
        "License exists": "LICENSE" in files,
        "Citation file exists": "CITATION.cff" in files,
        "Usage docs exist": "USAGE.md" in files or "docs/" in files,
        "Repo layout docs exist": "REPO_LAYOUT.md" in files,
        "Coding style docs exist": "RECOMMENDED_CODING_STYLE.md" in files,
        "CUDA/C++ source exists": "csrc/" in files,
        "Python package exists": "cula/" in files,
    }

    weights = {
        "README exists": 15,
        "Python packaging exists": 15,
        "Tests exist": 20,
        "License exists": 10,
        "Citation file exists": 5,
        "Usage docs exist": 10,
        "Repo layout docs exist": 5,
        "Coding style docs exist": 5,
        "CUDA/C++ source exists": 10,
        "Python package exists": 5,
    }

    score = sum(weights[k] for k, v in checks.items() if v)

    missing = [k for k, v in checks.items() if not v]

    return {
        **state,
        "quality_report": {
            "score": min(score, 100),
            "checks": checks,
            "missing": missing,
        }
    }
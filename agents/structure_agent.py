def detect_project_type(extension_counts, important_files):
    if ".cu" in extension_counts or "csrc/" in important_files:
        return "CUDA / High-performance Python package"
    if "package.json" in important_files:
        return "JavaScript / Web project"
    if "pyproject.toml" in important_files or "setup.py" in important_files:
        return "Python package"
    if "requirements.txt" in important_files:
        return "Python application"
    return "General software repository"


def structure_agent(state):
    files = state.get("important_files", {})
    extension_counts = state.get("extension_counts", {})

    checks = {
        "README present": "README.md" in files,
        "Dependency file present": any(x in files for x in ["requirements.txt", "pyproject.toml", "package.json"]),
        "Tests folder present": "tests/" in files,
        "Docs folder present": "docs/" in files,
        "Examples folder present": "examples/" in files,
        "Scripts folder present": "scripts/" in files,
        "License present": "LICENSE" in files,
        "Contributing guide present": "CONTRIBUTING.md" in files,
        "Environment template present": ".env.example" in files,
    }

    score = int((sum(checks.values()) / len(checks)) * 100)

    return {
        "structure_report": {
            "score": score,
            "project_type": detect_project_type(extension_counts, files),
            "checks": checks,
            "recommendations": [
                "Add examples/ with minimal runnable examples." if not checks["Examples folder present"] else "",
                "Add CONTRIBUTING.md for contributor onboarding." if not checks["Contributing guide present"] else "",
                "Add .env.example for environment variable documentation." if not checks["Environment template present"] else "",
            ],
        }
    }
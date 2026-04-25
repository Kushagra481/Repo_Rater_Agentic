def readme_agent(state):
    readme = state.get("important_files", {}).get("README.md", "")
    text = readme.lower()

    checks = {
        "Project title": readme.strip().startswith("#"),
        "Description": "description" in text or "overview" in text or len(readme) > 300,
        "Installation": "install" in text or "setup" in text or "pip" in text,
        "Usage": "usage" in text or "example" in text or "quickstart" in text,
        "Benchmarks": "benchmark" in text,
        "Tests": "test" in text or "pytest" in text,
        "Citation": "citation" in text or "cite" in text,
        "License": "license" in text,
    }

    score = int((sum(checks.values()) / len(checks)) * 100) if readme else 0
    missing = [k for k, v in checks.items() if not v]

    suggestions = []
    if "Installation" in missing:
        suggestions.append("Add exact installation commands for users.")
    if "Usage" in missing:
        suggestions.append("Add one minimal runnable example.")
    if "Benchmarks" in missing:
        suggestions.append("Add benchmark summary or link benchmark files.")
    if "Tests" in missing:
        suggestions.append("Add test running command such as pytest.")
    if "Citation" in missing:
        suggestions.append("Mention CITATION.cff in README.")

    return {
        **state,
        "readme_report": {
            "score": score,
            "checks": checks,
            "missing": missing,
            "suggestions": suggestions,
        }
    }
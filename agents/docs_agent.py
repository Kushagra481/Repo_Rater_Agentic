def docs_agent(state):
    files = state.get("important_files", {})
    readme = files.get("README.md", "")
    text = readme.lower()

    checks = {
        "Title": readme.strip().startswith("#"),
        "Description": "description" in text or "overview" in text or len(readme) > 300,
        "Installation": "install" in text or "setup" in text or "pip" in text,
        "Usage": "usage" in text or "quickstart" in text or "example" in text,
        "Architecture": "architecture" in text or "design" in text,
        "Testing instructions": "test" in text or "pytest" in text,
        "Benchmarks": "benchmark" in text,
        "Citation": "citation" in text or "cite" in text or "CITATION.cff" in files,
        "License mentioned": "license" in text or "LICENSE" in files,
    }

    score = int((sum(checks.values()) / len(checks)) * 100) if readme else 0

    recommendations = []
    if not checks["Installation"]:
        recommendations.append("Add exact installation commands.")
    if not checks["Usage"]:
        recommendations.append("Add a minimal usage example.")
    if not checks["Architecture"]:
        recommendations.append("Add architecture/design explanation.")
    if not checks["Testing instructions"]:
        recommendations.append("Add test-running instructions.")
    if not checks["Benchmarks"]:
        recommendations.append("Add benchmark explanation.")

    return {
        "docs_report": {
            "score": score,
            "checks": checks,
            "recommendations": recommendations,
        }
    }
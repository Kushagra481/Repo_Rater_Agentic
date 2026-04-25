def planner_agent(state):
    quality = state["quality_report"]
    readme = state["readme_report"]

    issues = []

    for missing in quality["missing"]:
        issues.append({
            "title": f"Improve repository: {missing}",
            "priority": "high" if "Tests" in missing or "packaging" in missing else "medium",
            "labels": ["repo-quality", "documentation"],
            "problem": f"The repository check failed for: {missing}.",
            "fix": f"Add or improve the missing component related to: {missing}."
        })

    for missing in readme["missing"]:
        issues.append({
            "title": f"Improve README section: {missing}",
            "priority": "medium",
            "labels": ["readme", "documentation"],
            "problem": f"The README is missing or weak in: {missing}.",
            "fix": f"Add a clear {missing} section with commands, examples, or explanations."
        })

    if not issues:
        issues.append({
            "title": "Add architecture diagram to documentation",
            "priority": "low",
            "labels": ["documentation", "enhancement"],
            "problem": "The repo is strong, but an architecture diagram would improve onboarding.",
            "fix": "Add a docs/architecture.md file with a module-level diagram."
        })

    return {
        **state,
        "issues": issues[:8]
    }
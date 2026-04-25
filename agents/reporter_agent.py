def bool_icon(value):
    return "✅" if value else "❌"


def reporter_agent(state):
    quality = state["quality_report"]
    readme = state["readme_report"]
    issues = state["issues"]

    # Format sections separately (IMPORTANT FIX)
    file_tree_block = "```txt\n" + state["file_tree"] + "\n```"

    quality_checks = "\n".join(
        f"- {bool_icon(v)} {k}" for k, v in quality["checks"].items()
    )

    readme_checks = "\n".join(
        f"- {bool_icon(v)} {k}" for k, v in readme["checks"].items()
    )

    issue_text = ""
    for i, issue in enumerate(issues, 1):
        issue_text += (
            f"\n### {i}. {issue['title']}\n\n"
            f"**Priority:** {issue['priority']}  \n"
            f"**Labels:** {', '.join(issue['labels'])}\n\n"
            f"**Problem:** {issue['problem']}\n\n"
            f"**Suggested Fix:** {issue['fix']}\n"
        )

    report = (
        "# RepoAgent Lite Report\n\n"
        "## Repository\n\n"
        f"{state['repo_url']}\n\n"
        "---\n\n"
        "## Overall Quality Score\n\n"
        f"**{quality['score']}/100**\n\n"
        "---\n\n"
        "## README Score\n\n"
        f"**{readme['score']}/100**\n\n"
        "---\n\n"
        "## File Tree\n\n"
        f"{file_tree_block}\n\n"
        "---\n\n"
        "## Repository Quality Checks\n\n"
        f"{quality_checks}\n\n"
        "---\n\n"
        "## README Checks\n\n"
        f"{readme_checks}\n\n"
        "---\n\n"
        "## Missing Repository Items\n\n"
        + ("\n".join("- " + x for x in quality["missing"]) if quality["missing"] else "- None")
        + "\n\n---\n\n"
        "## README Suggestions\n\n"
        + ("\n".join("- " + x for x in readme["suggestions"]) if readme["suggestions"] else "- README looks strong.")
        + "\n\n---\n\n"
        "## GitHub Issue Suggestions\n"
        f"{issue_text}\n"
        "---\n\n"
        "## Final Recommendation\n\n"
        "Improve onboarding, documentation, and test clarity. Add examples and architecture diagrams for better contributor experience.\n"
    )

    return {
        **state,
        "final_report": report
    }
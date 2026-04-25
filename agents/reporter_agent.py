def icon(value):
    return "✅" if value else "❌"


def format_checks(checks):
    if not checks:
        return "- No checks available."

    return "\n".join(f"- {icon(v)} {k}" for k, v in checks.items())


def format_list(items):
    if not items:
        return "- None"

    return "\n".join(f"- {item}" for item in items)


def format_issues(issues):
    if not issues:
        return "- No issues generated."

    text = ""

    for i, issue in enumerate(issues, 1):
        text += (
            f"\n### {i}. {issue['title']}\n\n"
            f"**Priority:** {issue['priority']}  \n"
            f"**Labels:** {', '.join(issue['labels'])}\n\n"
            f"**Problem:** {issue['problem']}\n\n"
            f"**Suggested Fix:** {issue['fix']}\n"
        )

    return text


def reporter_agent(state):
    structure = state.get("structure_report", {})
    docs = state.get("docs_report", {})
    code = state.get("code_report", {})
    security = state.get("security_report", {})
    merged = state.get("merged_report", {})
    issues = state.get("issues", [])

    file_tree_block = "```txt\n" + state.get("file_tree", "") + "\n```"

    report = (
        "# RepoAgent Lite Multi-Agent Report\n\n"
        "## Repository\n\n"
        f"{state.get('repo_url', '')}\n\n"
        "---\n\n"
        "## Final Multi-Agent Score\n\n"
        f"**{merged.get('overall_score', 0)}/100**\n\n"
        "---\n\n"
        "## Detected Project Type\n\n"
        f"**{structure.get('project_type', 'Unknown')}**\n\n"
        "---\n\n"
        "## Agent Scores\n\n"
        f"- Structure Agent: **{structure.get('score', 0)}/100**\n"
        f"- Documentation Agent: **{docs.get('score', 0)}/100**\n"
        f"- Code Agent: **{code.get('score', 0)}/100**\n"
        f"- Security Agent: **{security.get('score', 0)}/100**\n\n"
        "---\n\n"
        "## File Tree\n\n"
        f"{file_tree_block}\n\n"
        "---\n\n"
        "## Structure Agent Checks\n\n"
        f"{format_checks(structure.get('checks', {}))}\n\n"
        "---\n\n"
        "## Documentation Agent Checks\n\n"
        f"{format_checks(docs.get('checks', {}))}\n\n"
        "---\n\n"
        "## Code Agent Checks\n\n"
        f"{format_checks(code.get('checks', {}))}\n\n"
        "---\n\n"
        "## Security Agent Checks\n\n"
        f"{format_checks(security.get('checks', {}))}\n\n"
        "---\n\n"
        "## Strengths\n\n"
        f"{format_list(merged.get('strengths', []))}\n\n"
        "---\n\n"
        "## Weaknesses\n\n"
        f"{format_list(merged.get('weaknesses', []))}\n\n"
        "---\n\n"
        "## Recommendations\n\n"
        f"{format_list(merged.get('recommendations', []))}\n\n"
        "---\n\n"
        "## GitHub Issue Suggestions\n"
        f"{format_issues(issues)}\n\n"
        "---\n\n"
        "## Final Recommendation\n\n"
        "This repository was analyzed through a branching multi-agent workflow. "
        "The best next improvements are documentation clarity, contributor onboarding, "
        "test instructions, architecture explanation, and security hygiene checks.\n"
    )

    return {
        **state,
        "final_report": report
    }
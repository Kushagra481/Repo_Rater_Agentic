def merge_agent(state):
    structure = state.get("structure_report", {})
    docs = state.get("docs_report", {})
    code = state.get("code_report", {})
    security = state.get("security_report", {})

    scores = [
        structure.get("score", 0),
        docs.get("score", 0),
        code.get("score", 0),
        security.get("score", 0),
    ]

    overall_score = int(sum(scores) / len(scores))

    strengths = []
    weaknesses = []

    if structure.get("score", 0) >= 75:
        strengths.append("Repository structure is strong.")
    else:
        weaknesses.append("Repository structure needs improvement.")

    if docs.get("score", 0) >= 75:
        strengths.append("Documentation is strong.")
    else:
        weaknesses.append("Documentation needs improvement.")

    if code.get("score", 0) >= 75:
        strengths.append("Codebase organization looks healthy.")
    else:
        weaknesses.append("Codebase needs more tests or refactoring.")

    if security.get("score", 0) >= 75:
        strengths.append("Basic security hygiene looks acceptable.")
    else:
        weaknesses.append("Security hygiene needs improvement.")

    recommendations = []

    for report in [structure, docs, code, security]:
        for rec in report.get("recommendations", []):
            if rec:
                recommendations.append(rec)

    return {
        "merged_report": {
            "overall_score": overall_score,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations,
        }
    }
from pathlib import Path

SENSITIVE_PATTERNS = [
    "api_key",
    "secret_key",
    "password",
    "token",
    "private_key",
    "aws_access_key",
    "aws_secret",
]


def security_agent(state):
    repo_path = state.get("repo_path", "")
    files = state.get("important_files", {})
    findings = []

    if repo_path:
        root = Path(repo_path)

        for path in root.rglob("*"):
            if ".git" in path.parts or "__pycache__" in path.parts:
                continue

            if path.is_file() and path.suffix.lower() in [".py", ".env", ".txt", ".md", ".json", ".toml", ".yaml", ".yml"]:
                try:
                    text = path.read_text(encoding="utf-8", errors="ignore").lower()
                    for pattern in SENSITIVE_PATTERNS:
                        if pattern in text:
                            findings.append({
                                "file": str(path.relative_to(root)),
                                "pattern": pattern,
                            })
                            break
                except Exception:
                    pass

    checks = {
        ".env.example present": ".env.example" in files,
        ".gitignore present": ".gitignore" in files,
        "No obvious secret keywords found": len(findings) == 0,
    }

    score = int((sum(checks.values()) / len(checks)) * 100)

    recommendations = []
    if ".env.example" not in files:
        recommendations.append("Add .env.example.")
    if findings:
        recommendations.append("Review possible secret-like keywords.")

    return {
        "security_report": {
            "score": score,
            "checks": checks,
            "findings": findings[:10],
            "recommendations": recommendations,
        }
    }
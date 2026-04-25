def code_agent(state):
    stats = state.get("source_stats", {})
    extension_counts = state.get("extension_counts", {})
    files = state.get("important_files", {})

    total_source_files = stats.get("total_source_files", 0)
    large_files = stats.get("large_files", [])

    checks = {
        "Source files detected": total_source_files > 0,
        "No very large files": len(large_files) == 0,
        "Python files present": ".py" in extension_counts,
        "CUDA/C++ files present": any(ext in extension_counts for ext in [".cu", ".cpp", ".c", ".hpp", ".h"]),
        "Tests available": "tests/" in files,
    }

    score = int((sum(checks.values()) / len(checks)) * 100)

    recommendations = []
    if large_files:
        recommendations.append("Refactor very large files into smaller modules.")
    if not checks["Tests available"]:
        recommendations.append("Add tests for core logic.")
    if checks["CUDA/C++ files present"]:
        recommendations.append("Add CUDA/C++ build notes and GPU compatibility table.")

    return {
        "code_report": {
            "score": score,
            "checks": checks,
            "large_files": large_files[:10],
            "recommendations": recommendations,
        }
    }
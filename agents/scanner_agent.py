from tools.repo_loader import clone_repo
from tools.file_tree import generate_tree, collect_important_files, count_extensions, collect_source_stats


def scanner_agent(state):
    errors = state.get("errors", [])

    try:
        repo_path = clone_repo(state["repo_url"])

        return {
            **state,
            "repo_path": str(repo_path),
            "file_tree": generate_tree(repo_path),
            "important_files": collect_important_files(repo_path),
            "extension_counts": count_extensions(repo_path),
            "source_stats": collect_source_stats(repo_path),
            "errors": errors,
        }

    except Exception as e:
        errors.append(str(e))
        return {
            **state,
            "repo_path": "",
            "file_tree": "",
            "important_files": {},
            "extension_counts": {},
            "source_stats": {},
            "errors": errors,
        }
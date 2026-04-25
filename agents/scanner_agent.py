from tools.repo_loader import clone_repo
from tools.file_tree import generate_tree, important_files

def scanner_agent(state):
    try:
        path = clone_repo(state["repo_url"])
        return {
            **state,
            "repo_path": str(path),
            "file_tree": generate_tree(path),
            "important_files": important_files(path)
        }
    except Exception as e:
        state["errors"].append(str(e))
        return state
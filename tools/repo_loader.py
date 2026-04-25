from pathlib import Path
from git import Repo
import tempfile


def clone_repo(url: str) -> Path:
    temp_dir = Path(tempfile.mkdtemp(prefix="repo_agent_"))
    Repo.clone_from(url, temp_dir, depth=1)
    return temp_dir
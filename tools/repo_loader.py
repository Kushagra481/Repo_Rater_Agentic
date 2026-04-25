from git import Repo
import tempfile
from pathlib import Path

def clone_repo(url: str) -> Path:
    path = Path(tempfile.mkdtemp())
    Repo.clone_from(url, path, depth=1)
    return path
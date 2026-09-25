from pathlib import Path
from tempfile import TemporaryDirectory

from git import Repo


def clone_repository(
    github_url: str,
    destination: Path
) -> Path:
    destination.mkdir(
        parents=True,
        exist_ok=True
    )
    Repo.clone_from(
        github_url,
        destination,
        depth=1,
    )
    
    return destination

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Callable

from app.ingestion.clone import clone_repository
from app.ingestion.files import discover_source_files
from app.models.repository import Repository


def ingest_repository(
    repository: Repository,
    on_files_discovered: Callable[[list[Path]], None],
) -> None:
    with TemporaryDirectory(
        prefix="ai-code-ingestion-",
    ) as temporary_directory:
        repository_path = Path(temporary_directory)

        clone_repository(
            github_url=repository.github_url,
            destination=repository_path,
        )

        files = discover_source_files(
            repository_path,
        )

        on_files_discovered(files)
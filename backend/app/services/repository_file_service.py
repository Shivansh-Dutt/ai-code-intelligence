from pathlib import Path
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.repository_file import RepositoryFile
from app.ingestion.languages import detect_language


def create_repository_file(
    db: Session,
    repository_id: UUID,
    repository_root: Path,
    file_path: Path,
) -> RepositoryFile:
    relative_path = file_path.relative_to(
        repository_root
    ).as_posix()

    existing = db.scalar(
        select(RepositoryFile).where(
            RepositoryFile.repository_id == repository_id,
            RepositoryFile.path == relative_path,
        )
    )

    if existing is not None:
        return existing

    repository_file = RepositoryFile(
        repository_id=repository_id,
        path=relative_path,
        language=detect_language(file_path),
        size_bytes=file_path.stat().st_size,
    )

    db.add(repository_file)

    return repository_file
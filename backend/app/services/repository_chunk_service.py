from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ingestion.chunking import SourceChunk
from app.models.repository_chunk import RepositoryChunk


def create_repository_chunk(
    db: Session,
    file_id: UUID,
    chunk: SourceChunk,
) -> RepositoryChunk:
    existing = db.scalar(
        select(RepositoryChunk).where(
            RepositoryChunk.file_id == file_id,
            RepositoryChunk.start_line == chunk.start_line,
            RepositoryChunk.end_line == chunk.end_line
        )
    )
    
    if existing is not None:
        return existing
    
    repository_chunk = RepositoryChunk(
        file_id=file_id,
        start_line = chunk.start_line,
        end_line = chunk.end_line,
        content = chunk.content,
    )
    
    db.add(repository_chunk)
    
    return repository_chunk
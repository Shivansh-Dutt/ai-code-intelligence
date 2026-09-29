from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.repository_chunk import RepositoryChunk
from app.models.repository_file import RepositoryFile

from app.services.retrieval import RetrievalResult

def search_repository(
    db: Session,
    repository_id: UUID,
    query_embedding: list[float],
    limit: int = 10,
    max_distance: float = 0.65
) -> list[RetrievalResult]:
    distance = RepositoryChunk.embedding.cosine_distance(
        query_embedding
    )
    
    statement = (
        select(
            RepositoryChunk,
            RepositoryFile,
            distance.label("distance")
        )
        .join(
            RepositoryFile,
            RepositoryFile.id == RepositoryChunk.file_id,
        )
        .where(
            RepositoryFile.repository_id == repository_id,
            RepositoryChunk.embedding.is_not(None),
            distance <= max_distance
        )
        .order_by(distance)
        .limit(limit)
    )
    
    rows = db.execute(statement).all()

    return [
        RetrievalResult(
            chunk_id=chunk.id,
            file_id=file.id,
            path=file.path,
            start_line=chunk.start_line,
            end_line=chunk.end_line,
            content=chunk.content,
            distance=float(distance),
        )
        for chunk,file,distance in rows
    ]
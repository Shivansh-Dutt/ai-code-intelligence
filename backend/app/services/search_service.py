from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.repository_chunk import RepositoryChunk
from app.models.repository_file import RepositoryFile


def search_repository(
    db: Session,
    repository_id: UUID,
    query_embedding: list[float],
    limit: int = 10,
):
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
        )
        .order_by(distance)
        .limit(limit)
    )
    
    return db.execute(statement).all()
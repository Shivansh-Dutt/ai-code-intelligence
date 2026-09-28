from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.embeddings.huggingface_provider import (
    HuggingFaceEmbeddingProvider,
)
from app.services.search_service import search_repository


router = APIRouter(
    prefix="/api",
    tags=["search"],
)


@router.get(
    "/repositories/{repository_id}/search",
)
def semantic_search(
    repository_id: UUID,
    q: str,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    provider = HuggingFaceEmbeddingProvider()

    query_embedding = provider.embed(q)

    results = search_repository(
        db=db,
        repository_id=repository_id,
        query_embedding=query_embedding,
        limit=min(limit, 50),
    )

    return [
        {
            "file_id": file.id,
            "path": file.path,
            "start_line": chunk.start_line,
            "end_line": chunk.end_line,
            "content": chunk.content,
            "distance": float(distance),
        }
        for chunk, file, distance in results
    ]
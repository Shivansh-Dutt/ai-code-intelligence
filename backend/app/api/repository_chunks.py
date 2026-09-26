from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.repository_file import RepositoryFile
from app.models.repository_chunk import RepositoryChunk

router = APIRouter(
    prefix="/api",
    tags=["repository-chunks"],
)

@router.get(
    "/files/{file_id}/chunks",
)
def list_file_chunks(
    file_id: UUID,
    db: Session = Depends(get_db),
):
    file = db.get(
        RepositoryFile,
        file_id
    )
    
    if file is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repository file not found",
        )
        
    chunks = db.scalars(
        select(RepositoryChunk)
        .where(
            RepositoryChunk.file_id == file_id
        )
        .order_by(
            RepositoryChunk.start_line
        )
    ).all()
    
    return [
        {
            "id": chunk.id,
            "start_line": chunk.start_line,
            "end_line": chunk.end_line,
            "content": chunk.content,
        }
        for chunk in chunks
    ]
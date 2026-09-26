from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.repository import Repository
from app.models.repository_file import RepositoryFile


router = APIRouter(
    prefix="/api/repositories",
    tags=["repository-files"]
)

@router.get(
    "/{repository_id}/files"
)
def list_repository_files(
    repository_id: UUID,
    db: Session = Depends(get_db),
):
    repository = db.get(
        Repository,
        repository_id,
    )
    
    if repository is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repository not found"
        )
        
        
    files = db.scalars(
        select(RepositoryFile)
        .where(
            RepositoryFile.repository_id == repository_id
        )
        .order_by(RepositoryFile.path)
    ).all()
    
    return [
        {
            "id": file.id,
            "path": file.path,
            "language": file.language,
            "size_bytes": file.size_bytes,
        }
        for file in files
    ]
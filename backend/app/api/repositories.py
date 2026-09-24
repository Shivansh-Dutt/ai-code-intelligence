from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.repository import RepositoryCreate, RepositoryResponse
from app.services.repository_service import create_repository

router = APIRouter(
    prefix="/api/repositories",
    tags=["repositories"]
)

@router.post(
    "",
    response_model=RepositoryResponse,
    status_code=status.HTTP_201_CREATED,
)

def create_repository_endpoint(
    repository_data: RepositoryCreate,
    db: Session = Depends(get_db),   
) -> RepositoryResponse:
    return create_repository(
        db=db,
        repository_data=repository_data
    )
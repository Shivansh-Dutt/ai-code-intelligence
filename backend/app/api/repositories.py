from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.repository import RepositoryCreate, RepositoryResponse
from app.services.repository_service import (
    create_repository,
    get_repository,
    list_repositories,
)

from app.services.exceptions import RepositoryAlreadyExistsError

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
    try:
        return create_repository(
            db = db,
            repository_data=repository_data
        )
    except RepositoryAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc)
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        ) from exc
    
@router.get(
    "",
    response_model=list[RepositoryResponse]
)
def list_repositories_endpoint(
    db: Session = Depends(get_db),
) -> list[RepositoryResponse]:
    return list_repositories(db)


@router.get(
    "/{repository_id}",
    response_model=RepositoryResponse,
)
def get_repository_endpoint(
    repository_id: UUID,
    db: Session = Depends(get_db),
) -> RepositoryResponse:
    repository = get_repository(
        db=db,
        repository_id=repository_id
    )
    
    if repository is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repository not found"
        )
        
    return repository
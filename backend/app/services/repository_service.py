from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.repository import Repository
from app.schemas.repository import RepositoryCreate

from app.services.exceptions import RepositoryAlreadyExistsError
from app.services.github_url import validate_github_repository_url

def create_repository(
    db: Session,
    repository_data: RepositoryCreate,
) -> Repository:
    github_url = str(repository_data.github_url).rstrip("/")
    
    existing_repository = db.scalar(
        select(Repository).where(
            Repository.github_url == github_url
        )
    )
    
    if existing_repository is not None:
        raise RepositoryAlreadyExistsError(
            "Repository already exists"
        )
    
    # # temporary parsing
    # # proper github url parsing will be implmented in the ingestion phase
    # parts = github_url.rstrip("/").split("/")
    
    # owner = parts[-2]
    # name = parts[-1]
    
    owner, name = validate_github_repository_url(github_url)
    
    repository = Repository(
        github_url=github_url,
        owner = owner,
        name = name,
        status="pending"
    )
    
    db.add(repository)
    db.commit()
    db.refresh(repository)
    
    return repository

def get_repository(
    db: Session,
    repository_id: UUID,
) -> Repository | None:
    return db.scalar(
        select(Repository).where(
            Repository.id == repository_id
        )
    )
    
def list_repositories(
    db: Session,
) -> list[Repository]:
    return list(
        db.scalars(
            select(Repository).order_by(
                Repository.created_at.desc()
            )
        ).all()
    )
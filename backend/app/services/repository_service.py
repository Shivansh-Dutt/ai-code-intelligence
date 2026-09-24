from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.repository import Repository
from app.schemas.repository import RepositoryCreate

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
        return existing_repository
    
    # temporary parsing
    # proper github url parsing will be implmented in the ingestion phase
    parts = github_url.rstrip("/").split("/")
    
    owner = parts[-2]
    name = parts[-1]
    
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
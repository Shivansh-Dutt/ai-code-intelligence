from uuid import UUID

from pydantic import BaseModel, ConfigDict, HttpUrl

class RepositoryCreate(BaseModel):
    github_url: HttpUrl
    
class RepositoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    github_url: str
    owner: str
    name: str
    default_branch: str | None
    commit_sha: str | None
    status: str
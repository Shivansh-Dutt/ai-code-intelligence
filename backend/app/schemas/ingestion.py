from datetime import datetime
from uuid import UUID

from typing import Optional

from pydantic import BaseModel, ConfigDict

class IngestionJobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id : UUID
    repository_id : UUID
    status : str
    error_message : Optional[str | UUID] = None
    started_at : datetime | None
    completed_at : datetime | None
    created_at : datetime
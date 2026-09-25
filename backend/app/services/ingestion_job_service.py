from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ingestion_job import (
    IngestionJob,
    IngestionStatus
)


def create_ingestion_job(
    db: Session,
    repository_id: UUID
) -> IngestionJob:
    job = IngestionJob(
        repository_id=repository_id,
        status=IngestionStatus.PENDING
    )
    
    db.add(job)
    db.commit()
    db.refresh(job)
    
    return job

def get_ingestion_job(
    db: Session,
    job_id: UUID,
) -> IngestionJob | None:
    return db.scalar(
        select(IngestionJob).where(
            IngestionJob.id == job_id
        )
    )
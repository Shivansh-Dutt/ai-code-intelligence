from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.ingestion import IngestionJobResponse
from app.services.ingestion_job_service import (
    create_ingestion_job,
    get_ingestion_job,
)
from app.services.repository_service import get_repository
from app.workers.ingestion_worker import run_ingestion_job


router = APIRouter(
    prefix="/api",
    tags=["ingestion"],
)


@router.post(
    "/repositories/{repository_id}/ingest",
    response_model=IngestionJobResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def start_ingestion(
    repository_id: UUID,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> IngestionJobResponse:
    repository = get_repository(
        db=db,
        repository_id=repository_id,
    )

    if repository is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repository not found",
        )

    job = create_ingestion_job(
        db=db,
        repository_id=repository_id,
    )

    background_tasks.add_task(
        run_ingestion_job,
        job.id,
    )

    return job


@router.get(
    "/ingestion-jobs/{job_id}",
    response_model=IngestionJobResponse,
)
def get_ingestion_status(
    job_id: UUID,
    db: Session = Depends(get_db),
) -> IngestionJobResponse:
    job = get_ingestion_job(
        db=db,
        job_id=job_id,
    )

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingestion job not found",
        )

    return job
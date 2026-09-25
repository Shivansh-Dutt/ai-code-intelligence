from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.ingestion.clone import clone_repository
from app.ingestion.files import discover_source_files
from app.models.ingestion_job import (
    IngestionJob,
    IngestionStatus
)
from app.models.repository import Repository
from pathlib import Path
from tempfile import TemporaryDirectory

def run_ingestion_job(job_id: UUID) -> None:
    db: Session = SessionLocal()
    
    try:
        job = db.get(IngestionJob, job_id)
        
        if job is None:
            return
        
        repository = db.get(
            Repository,
            job.repository_id
        )
        
        if repository is None:
            job.status = IngestionStatus.FAILED
            job.error_message = "Repository not found"
            db.commit()
            return
        
        job.status = IngestionStatus.RUNNING
        job.started_at = datetime.now(timezone.utc)
        db.commit()
        
        with TemporaryDirectory(
            prefix="ai-code-ingestion-",
        ) as temporary_directory:
            repository_path = Path(
                temporary_directory
            )
            
            clone_repository(
                github_url=repository.github_url,
                destination=repository_path,
            )
            
            files = discover_source_files(
                repository_path,
            )
            
            print(
                f"Ingestion job {job.id}: "
                f"discovered {len(files)} source files"
            )
            
        job.status = IngestionStatus.COMPLETED
        job.completed_at = datetime.now(timezone.utc)
        db.commit()
    
    except Exception as exc:
        db.rollback()
        
        job = db.get(IngestionJob, job_id)
        
        if job is not None:
            job.status = IngestionStatus.FAILED
            job.error_message = str(exc)
            db.commit()
    
    finally:
        db.close()
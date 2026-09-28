from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import UUID

from app.db.session import SessionLocal
from app.ingestion.clone import clone_repository
from app.ingestion.files import discover_source_files
from app.models.ingestion_job import IngestionJob, IngestionStatus
from app.models.repository import Repository
from app.services.repository_file_service import create_repository_file
from sqlalchemy.orm import Session
from app.ingestion.content import read_source_file
from app.ingestion.chunking import chunk_source
from app.services.repository_chunk_service import (
    create_repository_chunk
)
from app.services.embedding_service import embed_chunks

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
            
            files = discover_source_files(
    repository_path,
)

            for file_path in files:
                repository_file = create_repository_file(
                    db=db,
                    repository_id=repository.id,
                    repository_root=repository_path,
                    file_path=file_path,
                )
                
                content = read_source_file(file_path)
                
                if content is None:
                    continue
                
                chunks = chunk_source(content)
                
                created_chunks = []
                
                for file_path in files:
                    repository_file = create_repository_file(
                        db=db,
                        repository_id=repository.id,
                        repository_root=repository_path,
                        file_path=file_path,
                    )
                
                    content = read_source_file(file_path)
                
                    if content is None:
                        continue
                    
                    chunks = chunk_source(content)
                
                    for chunk in chunks:
                        repository_chunk = create_repository_chunk(
                            db=db,
                            file_id=repository_file.id,
                            chunk=chunk,
                        )
                
                        created_chunks.append(repository_chunk)
                
                db.flush()
                
                chunks_to_embed = [
                    chunk
                    for chunk in created_chunks
                    if chunk.embedding is None
                ]
                
                embed_chunks(
                    db=db,
                    chunks=chunks_to_embed,
                )
                
            db.commit()
            
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
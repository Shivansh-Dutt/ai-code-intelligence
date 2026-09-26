from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class RepositoryChunk(Base):
    __tablename__ = "repository_chunks"
    
    __table_args__ = (
        UniqueConstraint(
            "file_id",
            "start_line",
            "end_line",
            name="uq_repository_chunk_location"
        ),
    )
    
    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    
    file_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey("repository_files.id"),
        nullable=False,
    )
    
    start_line: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    
    end_line: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
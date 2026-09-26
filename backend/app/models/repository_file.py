from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func , UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class RepositoryFile(Base):
    __tablename__ = "repository_files"

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    repository_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey("repositories.id"),
        nullable=False,
    )

    path: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    language: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    size_bytes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    
    __table_args__ = (
        UniqueConstraint(
            "repository_id",
            "path",
            name="uq_repository_file_path",
        ),
    )
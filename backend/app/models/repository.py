from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class Repository(Base):
    __tablename__ = "repositories"
    
    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    
    github_url: Mapped[str] = mapped_column(
        Text,
        unique=True,
        nullable=False,
    )
    
    owner: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    
    default_branch: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )
    
    commit_sha: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True
    )
    
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="pending"
    )
    
    created_at: Mapped[str] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
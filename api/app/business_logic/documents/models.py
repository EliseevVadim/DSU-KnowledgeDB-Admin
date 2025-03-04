import uuid
from typing import Optional

from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from app.database import EmbeddingBase


class Document(EmbeddingBase):
    __tablename__ = 'langchain_pg_embedding'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    document: Mapped[str] = mapped_column(nullable=False)
    cmetadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

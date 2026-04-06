from sqlalchemy import Column, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, JSON, TSVECTOR
from pgvector.sqlalchemy import Vector
from src.models.base import Base


class Embedding(Base):
    __tablename__ = 'embedding'
    uuid = Column(UUID, primary_key=True, index=True)
    file_id = Column(UUID)
    chunk_id = Column(UUID)
    collection_id = Column(UUID)
    embedding_vector = Column(Vector(1536))
    search_vector = Column(TSVECTOR)
    cmetadata = Column(JSON)
    create_time = Column(TIMESTAMP(timezone=True), nullable=False)

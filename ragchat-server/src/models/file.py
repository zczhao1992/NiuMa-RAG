from sqlalchemy import Column, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, VARCHAR, JSON
from src.models.base import Base


class File(Base):
    __tablename__ = 'file'
    uuid = Column(UUID, primary_key=True, index=True)
    create_time = Column(TIMESTAMP(timezone=True), nullable=False)
    collection_id = Column(UUID)
    file_extension = Column(VARCHAR)
    cmetadata = Column(JSON)

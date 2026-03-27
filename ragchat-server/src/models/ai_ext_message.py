from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from src.models.base import Base


class AiExtMessage(Base):
    __tablename__ = 'ai_ext_message'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    run_id = Column(String, unique=False, index=True)
    ext_context = Column(String)

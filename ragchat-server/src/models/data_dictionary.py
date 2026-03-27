from sqlalchemy import Column, Integer, String

from src.models.base import Base


class DataDictionary(Base):
    __tablename__ = 'data_dictionary'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    key = Column(String, unique=True, index=True)
    value = Column(String)

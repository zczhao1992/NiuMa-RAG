from sqlalchemy import Column, Integer, String
from src.models.base import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(50), nullable=False)

    def __repr__(self):
        return f"<User(id='{self.id}', name='{self.name}')>"

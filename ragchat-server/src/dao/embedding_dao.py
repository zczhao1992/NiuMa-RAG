from sqlalchemy.ext.asyncio import AsyncSession
from src.dao.base_dao import BaseDao
from src.models.embedding import Embedding


class EmbeddingDao(BaseDao):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Embedding)

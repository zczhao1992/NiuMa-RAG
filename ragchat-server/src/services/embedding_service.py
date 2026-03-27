from sqlalchemy.ext.asyncio import AsyncSession
from src.dao.embedding_dao import EmbeddingDao
from src.dto.embedding_dto import EmbeddingDto
from src.services.base_service import BaseService


class EmbeddingService(BaseService):

    def __init__(self, db: AsyncSession):
        super().__init__(EmbeddingDao(db), EmbeddingDto)

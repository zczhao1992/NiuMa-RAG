from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.dao.embedding_dao import EmbeddingDao
from src.dto.embedding_dto import EmbeddingDto
from src.services.base_service import BaseService


class EmbeddingService(BaseService):

    def __init__(self, db: AsyncSession):
        super().__init__(EmbeddingDao(db), EmbeddingDto)
        self.dao: EmbeddingDao = self.dao

    async def batch_embedding_create(self, data: list[EmbeddingDto]):
        return await self.dao.batch_embedding_create(data)

    async def delete_embedding_by_file_id(self, file_id: UUID):
        return await self.dao.delete_embedding_by_file_id(file_id)

from sqlalchemy.ext.asyncio import AsyncSession
from src.dao.chunk_dao import ChunkDao
from src.dto.chunk_dto import ChunkDto
from src.services.base_service import BaseService


class ChunkService(BaseService):

    def __init__(self, db: AsyncSession):
        super().__init__(ChunkDao(db), ChunkDto)

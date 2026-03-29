import os

from sqlalchemy import delete, select, UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.dao.base_dao import BaseDao
from src.models.chunk import Chunk
from src.utils.sql_template_manager import SQLTemplateManager


class ChunkDao(BaseDao):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Chunk, primary_key="uuid")
        self.sql_template_manager = SQLTemplateManager(
            os.path.dirname(__file__))

    async def get_by_file_id(self, file_id: UUID):
        result = await self.db.execute(
            select(Chunk)
            .where(Chunk.file_id == file_id)
            .order_by(Chunk.index)
        )
        return result.scalars().all()

    async def get_chunks_by_ids(self, chunk_ids: list[UUID]):
        if not chunk_ids:
            return []
        stmt = select(Chunk).where(Chunk.uuid.in_(chunk_ids))
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def delete_by_file_id(self, file_id: str) -> bool:

        stmt = delete(Chunk).where(Chunk.file_id == file_id)
        await self.db.execute(stmt)

        return True

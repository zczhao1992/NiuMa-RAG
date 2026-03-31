from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.dao.chunk_dao import ChunkDao
from src.dto.chunk_dto import ChunkDto
from src.services.base_service import BaseService
from src.dto.chunk_embedding_dto import ChunkEmbeddingDto


class ChunkService(BaseService):

    def __init__(self, db: AsyncSession):
        super().__init__(ChunkDao(db), ChunkDto)
        self.dao: ChunkDao = self.dao

    async def get_chunks_by_file_id(self, file_id: UUID) -> list[ChunkDto]:
        chunks = await self.dao.get_by_file_id(file_id)
        return [
            ChunkDto(
                uuid=chunk.uuid,
                file_id=chunk.file_id,
                file_name=chunk.file_name,
                context=chunk.context,
                index=chunk.index,
                status=chunk.status,
                create_time=chunk.create_time
            ) for chunk in chunks
        ]

    async def get_chunks_by_ids(self, chunk_ids: list[UUID]):
        chunks = await self.dao.get_chunks_by_ids(chunk_ids)
        return [
            ChunkDto(
                uuid=chunk.uuid,
                file_id=chunk.file_id,
                file_name=chunk.file_name,
                context=chunk.context,
                index=chunk.index,
                status=chunk.status,
                create_time=chunk.create_time
            ) for chunk in chunks
        ]

    async def query_embedding_chunks(self):
        results = await self.dao.query_embedding_chunks()
        if results:
            return [ChunkEmbeddingDto.model_validate(result) for result in results]
        return None

    async def batch_update_status_by_uuids(self, uuids: list[UUID], new_status: int):
        await self.dao.batch_update_status_by_uuids(uuids, new_status)

    async def delete_chunks_by_file_id(self, file_id: str) -> bool:

        if not file_id:
            return False

        return await self.dao.delete_chunks_by_file_id(file_id)

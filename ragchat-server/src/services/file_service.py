from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.dao.file_dao import FileDao
from src.dto.file_dto import FileDto
from src.services.base_service import BaseService


class FileService(BaseService):

    def __init__(self, db: AsyncSession):
        super().__init__(FileDao(db), FileDto)
        self.dao: FileDao = self.dao

    async def query_files(self, collection_id: str):
        results = await self.dao.query_files(collection_id)
        if results:
            return [FileDto.model_validate(result) for result in results]
        return None

    async def delete_file(self, file_id: UUID):
        await self.delete_by_id(file_id)
        return True

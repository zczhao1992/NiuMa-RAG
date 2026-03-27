from sqlalchemy.ext.asyncio import AsyncSession
from src.dao.file_dao import FileDao
from src.dto.file_dto import FileDto
from src.services.base_service import BaseService


class FileService(BaseService):

    def __init__(self, db: AsyncSession):
        super().__init__(FileDao(db), FileDto)

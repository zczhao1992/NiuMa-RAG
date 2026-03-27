from sqlalchemy.ext.asyncio import AsyncSession
from src.dao.data_dictionary_dao import DataDictionaryDao
from src.dto.data_dictionary_dto import DataDictionaryDto
from src.services.base_service import BaseService


class DataDictionaryService(BaseService):

    def __init__(self, db: AsyncSession):
        super().__init__(DataDictionaryDao(db), DataDictionaryDto)

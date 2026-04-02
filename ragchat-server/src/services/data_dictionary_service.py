from sqlalchemy.ext.asyncio import AsyncSession
from src.dao.data_dictionary_dao import DataDictionaryDao
from src.dto.data_dictionary_dto import DataDictionaryDto
from src.services.base_service import BaseService


class DataDictionaryService(BaseService):

    def __init__(self, db: AsyncSession):
        super().__init__(DataDictionaryDao(db), DataDictionaryDto)
        self.dao: DataDictionaryDao = self.dao

    async def get_by_key(self, key: str):
        dict = await self.dao.get_by_key(key)

        if dict:
            return DataDictionaryDto.model_validate(dict)
        return None

    async def batch_upsert_dicts(self, items: list[dict]):
        await self.dao.batch_upsert_dicts(items)

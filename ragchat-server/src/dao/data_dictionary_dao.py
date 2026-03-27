from sqlalchemy.ext.asyncio import AsyncSession
from src.dao.base_dao import BaseDao
from src.models.data_dictionary import DataDictionary


class DataDictionaryDao(BaseDao):
    def __init__(self, db: AsyncSession):
        super().__init__(db, DataDictionary)

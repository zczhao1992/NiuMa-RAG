from sqlalchemy.ext.asyncio import AsyncSession
from src.dao.base_dao import BaseDao
from src.models.data_dictionary import DataDictionary
from sqlalchemy import select, update, delete


class DataDictionaryDao(BaseDao):
    def __init__(self, db: AsyncSession):
        super().__init__(db, DataDictionary)

    async def get_by_key(self, key: str):
        result = await self.db.execute(select(DataDictionary).where(DataDictionary.key == key))
        return result.scalar_one_or_none()

    async def batch_upsert_dicts(self, items: list[dict]):
        for item in items:
            query = (
                update(DataDictionary)
                .where(DataDictionary.key == item["key"])
                .values(value=item["value"])
                .returning(DataDictionary.id)
            )
            result = await self.db.execute(query)

            if result.scalar_one_or_none() is None:
                dict_item = DataDictionary(
                    key=item["key"], value=item["value"])
                self.db.add(dict_item)
        await self.db.commit()

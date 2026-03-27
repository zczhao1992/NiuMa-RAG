from sqlalchemy.ext.asyncio import AsyncSession
from src.dao.base_dao import BaseDao
from src.models.collection import Collection


class CollectionDao(BaseDao):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Collection)

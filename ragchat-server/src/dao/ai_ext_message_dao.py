from sqlalchemy.ext.asyncio import AsyncSession
from src.dao.base_dao import BaseDao
from src.models.ai_ext_message import AiExtMessage


class AiExtMessageDao(BaseDao):
    def __init__(self, db: AsyncSession):
        super().__init__(db, AiExtMessage)

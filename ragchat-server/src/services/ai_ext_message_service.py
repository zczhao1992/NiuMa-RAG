from sqlalchemy.ext.asyncio import AsyncSession
from src.dao.ai_ext_message_dao import AiExtMessageDao
from src.dto.ai_ext_message_dto import AiExtMessageDto
from src.services.base_service import BaseService


class AiExtMessageService(BaseService):

    def __init__(self, db: AsyncSession):
        super().__init__(AiExtMessageDao(db), AiExtMessageDto)

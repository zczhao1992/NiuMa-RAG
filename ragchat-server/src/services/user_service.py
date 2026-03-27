from sqlalchemy.ext.asyncio import AsyncSession
from src.dao.user_dao import UserDao
# from singleton_decorator import singleton
from src.dto.user_dto import UserDto
from src.services.base_service import BaseService


class UserService(BaseService):

    def __init__(self, db: AsyncSession):
        super().__init__(UserDao(db), UserDto)

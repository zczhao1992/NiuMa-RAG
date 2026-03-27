from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.pg_db import get_db
from src.core.api_contract import APIContract
from src.services.user_service import UserService

router = APIRouter(tags=['user'], prefix="/user")


@router.get("/")
async def get_all_users(db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    users = await user_service.get_all()
    return APIContract.success(users)

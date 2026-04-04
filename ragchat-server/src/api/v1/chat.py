from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.api_contract import APIContract
from src.db.pg_db import get_db
from src.handler.chat_model_handler import ChatModelHandler
from src.services.user_service import UserService

router = APIRouter(tags=['chat'], prefix="/chat")


class ChatRequest(BaseModel):
    user_id: str
    message: str
    collection_id: str


@router.post("/")
async def chat_with_user(req: ChatRequest, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    user = await user_service.get_by_id(req.user_id)

    if not user:
        return APIContract.error("user not found")

    chat_model_handler = ChatModelHandler()

    if not req.collection_id:
        response = await chat_model_handler.get_llm_response(req.user_id, req.message)
    else:
        response = await chat_model_handler.get_llm_rag_response(req.user_id, req.collection_id, req.message)

    if not response:
        return APIContract.error("AI大模型会话失败")

    return APIContract.success(response)

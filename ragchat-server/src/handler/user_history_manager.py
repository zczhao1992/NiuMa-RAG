from src.db.pg_db import create_async_connection
from langchain_community.chat_message_histories import PostgresChatMessageHistory


class UserHistoryManager:
    def __init__(self):
        pass

    async def get_user_chat_history(self, user_id: str):
        try:
            async_connection = await create_async_connection()
        except Exception as e:
            raise

        history = PostgresChatMessageHistory(
            table_name="user_history",
            session_id=user_id,
            connection_string=async_connection
        )

        return history

    async def get_user_history_messages(self, user_id: str):
        history = await self.get_user_chat_history(user_id)
        messages = await history.aget_messages()

        if messages is None or len(messages) == 0:
            return []

        return messages

    async def delete_user_history_messages(self, user_id: str):
        history = await self.get_user_chat_history(user_id)
        await history.aclear()

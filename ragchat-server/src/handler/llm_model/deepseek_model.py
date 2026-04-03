from src.db.pg_db import get_db
from src.handler.llm_model.base_model import BaseModel
from src.services.data_dictionary_service import DataDictionaryService
from langchain_deepseek import ChatDeepSeek


class DeepSeekModel(BaseModel):

    def __init__(self):
        self.llm = None

    async def init_llm_model(self):
        async for db_session in get_db():
            dict_service = DataDictionaryService(db_session)
            dict = await dict_service.get_by_key("deepseek_api_key")
            api_key = dict.value if dict else None

            dict = await dict_service.get_by_key("temperature")
            temperature = dict.value if dict else "0.5"

            if api_key:
                self.llm = ChatDeepSeek(
                    model="deepseek-chat", temperature=float(temperature), api_key=api_key)

        return self.llm

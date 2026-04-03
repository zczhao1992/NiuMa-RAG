from src.db.pg_db import get_db
from src.handler.llm_model.base_model import BaseModel
from src.services.data_dictionary_service import DataDictionaryService
from langchain_openai import ChatOpenAI


class OpenAIModel(BaseModel):

    def __init__(self):
        self.llm = None

    async def init_llm_model(self):

        openai_api_key = None
        openai_base_url = None
        temperature = "0.5"

        async for db_session in get_db():
            dict_service = DataDictionaryService(db_session)

            dict_key = await dict_service.get_by_key("openai_api_key")
            openai_api_key = dict_key.value if dict_key else None

            dict_base = await dict_service.get_by_key("openai_api_base")
            openai_base_url = dict_base.value if dict_base else None

            dict_temp = await dict_service.get_by_key("temperature")
            temperature = dict.value if dict_temp else "0.5"

            if openai_api_key:
                self.llm = ChatOpenAI(
                    model="gpt-4",
                    temperature=float(temperature),
                    openai_api_base=openai_base_url,
                    openai_api_key=openai_api_key)

        return self.llm

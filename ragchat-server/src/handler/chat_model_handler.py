from src.db.pg_db import get_db
from src.handler.llm_model.llm_factory import LLMFactory
from src.handler.prompt.prompt_template import CustomPromptTemplate
from src.services.data_dictionary_service import DataDictionaryService
from langchain_core.messages import AIMessage, HumanMessage


class ChatModelHandler:
    def __init__(self):
        pass

    async def _init_llm(self):
        llm_model = None

        async for db_session in get_db():
            dict_service = DataDictionaryService(db_session)
            dict = await dict_service.get_by_key("llm_model")
            llm_model = dict.value if dict else None

        if llm_model is None:
            raise Exception("LLM_MODEL not found")

        llm_instance = LLMFactory.create_model(llm_model)
        return await llm_instance.init_llm_model()

    async def init_chain(self, is_rag=False):
        llm = await self._init_llm()

        prompt = await CustomPromptTemplate().create_prompt(is_rag)

        chain = prompt | llm

        return chain

    async def get_llm_response(self, user_id, message):
        user_message = HumanMessage(content=message)
        chain = await self.init_chain(False)

        response = await chain.ainvoke({"question": user_message})
        result = {}

        if isinstance(response, AIMessage):
            result["content"] = response.content
        else:
            raise ValueError("AI大模型返回的不是 AIMessage 类型")

        return result

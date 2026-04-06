from src.db.pg_db import get_db
from src.services.data_dictionary_service import DataDictionaryService
from langchain_core.prompts import ChatPromptTemplate


class CustomPromptTemplate:
    def __init__(self):
        pass

    async def _get_system_prompt(self, is_rag: False):
        async for db_session in get_db():
            dict_service = DataDictionaryService(db_session)

            dict = await dict_service.get_by_key("prompt_system" if not is_rag else "prompt_system_rag")
            system_message = dict.value if dict else None

            if not system_message:
                raise ValueError("提示词未设置")

            return system_message

    async def create_prompt(self, is_rag: False):
        system_prompt = await self._get_system_prompt(is_rag)

        if is_rag:
            # prompt_template = system_prompt + """
            #     请根据提下文档回答问题：{context}
            #     问题：{question}
            # """
            # prompt = PromptTemplate(
            #     template=prompt_template, input_variables=[
            #         "context", "question"]
            # )
            prompt = ChatPromptTemplate([
                ("system", system_prompt),
                # ("user", "请根据一下文档回答问题: {context}\n\n{question}")
                ("user",
                 "历史对话: \n{chat_history}\n\n参考文档: {context}\n\n用户问题: {question}\n\n请根据以上文档和历史对话回答问题:")
            ])
            return prompt
        else:
            # prompt_template = system_prompt + """
            #     问题：{question}
            # """
            # prompt = PromptTemplate(
            #     template=prompt_template, input_variables=["question"]
            # )

            prompt = ChatPromptTemplate([
                ("system", system_prompt),
                # ("user", "{question}")
                ("user",
                 "历史对话：\n{chat_history}\n\n用户问题: \n{question}\n\n请基于对话历史回答问题:")
            ])

            return prompt

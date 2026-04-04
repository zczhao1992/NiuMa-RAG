import asyncio
from src.db.pg_db import get_db
from src.handler.llm_model.llm_factory import LLMFactory
from src.handler.prompt.prompt_template import CustomPromptTemplate
from src.services.data_dictionary_service import DataDictionaryService
from langchain_core.messages import AIMessage, HumanMessage
from src.handler.search import search_handler_map, SearchMode
from src.services.chunk_service import ChunkService


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

    async def get_llm_rag_response(self, user_id, collection_id, message):
        user_message = HumanMessage(content=message)
        chain = await self.init_chain(True)

        async for db_session in get_db():
            dict_service = DataDictionaryService(db_session)
            search_mode_dict = await dict_service.get_by_key("search_mode")
            top_dict = await dict_service.get_by_key("top_n")
            threshold_vector_dict = await dict_service.get_by_key("threshold_vector")
            threshold_fulltext_dict = await dict_service.get_by_key("threshold_fulltext")

        search_mode = search_mode_dict.value if search_mode_dict else None
        top_n = int(top_dict.value) if top_dict else 5
        threshold_vector = float(
            threshold_vector_dict.value) if threshold_vector_dict and threshold_vector_dict.value else 0.5
        threshold_fulltext = float(
            threshold_fulltext_dict.value) if threshold_fulltext_dict and threshold_fulltext_dict.value else 0.05

        chunk_ids = await self._retrieve_chunk_ids(
            collection_id, message, search_mode, top_n,
            threshold_vector, threshold_fulltext
        )

        context_str = await self._build_context(chunk_ids)

        response = await chain.ainvoke({"question": user_message, "context": context_str})
        result = {}

        if isinstance(response, AIMessage):
            result["content"] = response.content
        else:
            raise ValueError("AI大模型返回的不是 AIMessage 类型")
        return result

    async def _retrieve_chunk_ids(self, collection_id, message, search_mode, top_n,
                                  threshold_vector, threshold_fulltext):
        chunk_ids = []
        if search_mode == "fulltext":
            search_result = await search_handler_map["fulltext"].handle(
                collection_id, message, top_n, threshold_fulltext, threshold_vector
            )

            if search_result:
                chunk_ids.extend([item["chunk_id"] for item in search_result])

        elif search_mode == "embedding":
            search_result = await search_handler_map["embedding"].handle(
                collection_id, message, top_n, threshold_vector, search_mode
            )
            if search_result:
                chunk_ids.extend([item["chunk_id"] for item in search_result])

        elif search_mode == "hybrid":
            search_vector_result, search_fulltext_result = await asyncio.gather(
                search_handler_map[SearchMode.EMBEDDING].handle(
                    collection_id, message, top_n, threshold_vector, SearchMode.EMBEDDING
                ),
                search_handler_map[SearchMode.FULLTEXT].handle(
                    collection_id, message, top_n, threshold_vector, SearchMode.FULLTEXT
                )
            )

            if search_vector_result:
                chunk_ids.extend([item["chunk_id"]
                                 for item in search_vector_result])

            if search_fulltext_result:
                chunk_ids.extend([item["chunk_id"]
                                 for item in search_fulltext_result])

        unique_chunk_ids = list(dict.fromkeys(chunk_ids))

        return unique_chunk_ids

    async def _build_context(self, chunk_ids):
        if not chunk_ids:
            return ""

        context_list = []

        async for db_session in get_db():
            chunk_service = ChunkService(db_session)
            chunks = await chunk_service.get_chunks_by_ids(chunk_ids)
            for chunk in chunks:
                context_list.append(chunk.context)

        context_str = "\n".join(context_list)

        return context_str

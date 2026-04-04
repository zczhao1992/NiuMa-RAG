from enum import StrEnum
import os
from jinja2 import Environment, FileSystemLoader
from sqlalchemy import text
from abc import ABC, abstractmethod
from src.config.conf import PROJECT_DIR
from src.core.embedding_manager import get_embeddings
from src.db.pg_db import get_db
from src.utils.sql_template_manager import SQLTemplateManager
from src.utils.jieba_tool import to_query


class SearchMode(StrEnum):
    EMBEDDING = "embedding"
    FULLTEXT = "fulltext"
    HYBRID = "hybrid"


class ISearch(ABC):
    @abstractmethod
    def support(self, search_mode: SearchMode):
        pass

    @abstractmethod
    async def handle(self, collection_id, query_text, top_n: int,
                     score_threshold: float, search_mode: SearchMode):
        pass


class FullTextSearch(ISearch):
    async def handle(self, collection_id, query_text, top_n: int, score_threshold: float, search_mode: SearchMode):
        try:
            if self.support(search_mode):
                sql_template = SQLTemplateManager(
                    os.path.join(PROJECT_DIR, "src", "dao", "sql"))
                sql = sql_template.render_sql(
                    "fulltext_search.sql.j2", collection_id=collection_id,
                    query=to_query(query_text),
                    top_n=top_n,
                    full_srore_threshold=score_threshold
                )

                async for session in get_db():
                    result = await session.execute(text(sql))

                columns = result.keys()

                rows = [dict(zip(columns, row)) for row in result.fetchall()]
                return rows
            else:
                return []
        except FileNotFoundError:
            raise
        except Exception as e:
            raise
        return []

    def support(self, search_mode: SearchMode):
        return search_mode == SearchMode.FULLTEXT


class EmbeddingSearch(ISearch):
    async def handle(self, collection_id, query_text, top_n: int, score_threshold: float, search_mode: SearchMode):
        try:
            if self.support(search_mode):
                embedding_model = get_embeddings()
                query_embedding = embedding_model.embed_query(query_text)

                sql_template = SQLTemplateManager(
                    os.path.join(PROJECT_DIR, "src", "dao", "sql"))
                sql = sql_template.render_sql(
                    "embedding_search.sql.j2", collection_id=collection_id,
                    top_n=top_n,
                    query_embedding=query_embedding,
                    vector_score_threshold=score_threshold,
                )

                async for session in get_db():
                    result = await session.execute(text(sql))

                columns = result.keys()

                rows = [dict(zip(columns, row)) for row in result.fetchall()]
                return rows
            else:
                return []
        except FileNotFoundError:
            raise
        except Exception as e:
            raise
        return []

    def support(self, search_mode: SearchMode):
        return search_mode == SearchMode.EMBEDDING


search_handler_map = {
    "embedding": EmbeddingSearch(),
    "fulltext": FullTextSearch()
}

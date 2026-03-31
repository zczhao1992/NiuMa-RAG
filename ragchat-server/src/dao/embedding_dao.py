import json
import uuid
from sqlalchemy import UUID, delete, text
from sqlalchemy.ext.asyncio import AsyncSession
from src.dao.base_dao import BaseDao
from src.models.embedding import Embedding
from src.utils.jieba_tool import clean_text
from datetime import datetime


def json_serializer(obj):
    """
    鲁棒性更强的 JSON 序列化器
    """
    # 1. 只要有 hex 属性，基本就是某种 UUID 类
    if hasattr(obj, "hex"):
        return str(obj)

    # 2. 显式判断内置的 uuid.UUID
    if isinstance(obj, uuid.UUID):
        return str(obj)

    # 3. 处理时间
    if isinstance(obj, datetime):
        return obj.isoformat()

    # 4. 特殊处理：如果对象有 dict 方法（针对某些 DTO 或 Model）
    if hasattr(obj, "dict"):
        return obj.dict()

    raise TypeError(
        f"Object of type {obj.__class__.__name__} is not JSON serializable")


class EmbeddingDao(BaseDao):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Embedding, primary_key="uuid")

    async def delete_embedding_by_file_id(self, file_id: UUID):
        await self.db.execute(delete(self.model).where(self.model.file_id == file_id))
        await self.db.commit()

    async def batch_embedding_create(self, items: list):
        print(f"DEBUG: 准备发送到 SQL 的数据样例: {items[0]}")
        data = [
            {
                "uuid": item.uuid,
                "file_id": item.file_id,
                "chunk_id": item.chunk_id,
                "collection_id": item.collection_id,
                "embedding_vector": item.embedding_vector.to_list(),
                "search_vector": clean_text(item.search_vector),
                "cmetadata": item.cmetadata,
                "create_time": item.create_time
            }
            for item in items
        ]

        insert_sql = text(
            """
            INSERT INTO embedding (uuid, file_id, chunk_id, collection_id, embedding_vector, search_vector,cmetadata,create_time)
            SELECT
                (element->>'uuid')::UUID,
                (element->>'file_id')::UUID,
                (element->>'chunk_id')::UUID,
                (element->>'collection_id')::UUID,
                (element->>'embedding_vector')::VECTOR,
                to_tsvector('simple', element->>'search_vector'),
                (element->'cmetadata')::JSONB,
                (element->>'create_time')::TIMESTAMP WITH TIME ZONE
            FROM json_array_elements(:data) AS element
            """
        )
        print(f"=================================================")
        await self.db.execute(insert_sql, {"data": json.dumps(data, default=json_serializer)})
        await self.db.commit()

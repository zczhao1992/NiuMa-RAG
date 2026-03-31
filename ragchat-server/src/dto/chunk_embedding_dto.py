from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional


class ChunkEmbeddingDto(BaseModel):
    # 允许从 SQLAlchemy 模型对象直接转换
    model_config = ConfigDict(from_attributes=True)

    chunk_id: UUID
    context: str
    file_id: UUID
    collection_id: UUID
    # 如果你的 SQL 查询结果里包含文件名或状态，也可以加上
    file_name: Optional[str] = None

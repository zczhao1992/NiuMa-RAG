from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime


class ChunkDto(BaseModel):
    uuid: UUID
    file_id: UUID
    file_name: Optional[str]
    context: str
    index: int
    status: int
    create_time: datetime

    model_config = {
        "from_attributes": True,
    }

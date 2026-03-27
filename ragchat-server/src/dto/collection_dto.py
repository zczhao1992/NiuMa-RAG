from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime


class CollectionDto(BaseModel):
    uuid: UUID
    name: Optional[str]
    cmetadata: Optional[str]
    create_time: datetime

    model_config = {
        "from_attributes": True,
    }

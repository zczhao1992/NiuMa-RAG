from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime


class FileDto(BaseModel):
    uuid: UUID
    file_name: str
    file_extension: Optional[str]
    collection_id: Optional[UUID]
    cmetadata: Optional[str]
    create_time: datetime

    model_config = {
        "from_attributes": True,
    }

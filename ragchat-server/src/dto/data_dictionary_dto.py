from pydantic import BaseModel
from typing import Optional


class DataDictionaryDto(BaseModel):
    id: int
    key: str
    value: Optional[str]

    model_config = {
        "from_attributes": True,
    }

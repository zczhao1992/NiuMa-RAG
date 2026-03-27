from pydantic import BaseModel
from typing import Optional


class AiExtMessageDto(BaseModel):
    id: int
    run_id: Optional[str]
    ext_context: Optional[str]

    model_config = {
        "from_attributes": True,
    }

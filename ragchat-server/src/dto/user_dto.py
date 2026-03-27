from pydantic import BaseModel


class UserDto(BaseModel):
    id: str
    name: str

    model_config = {
        "from_attributes": True
    }

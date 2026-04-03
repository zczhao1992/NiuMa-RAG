from abc import ABC, abstractmethod


class BaseModel(ABC):

    @classmethod
    @abstractmethod
    async def init_llm_model(cls):
        pass

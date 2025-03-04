from abc import ABC, abstractmethod
from typing import Any


class AsyncBaseService(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @abstractmethod
    async def __call__(self, *args, **kwargs) -> Any:
        pass

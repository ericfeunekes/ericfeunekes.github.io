from contextlib import asynccontextmanager
from asyncio import Semaphore, sleep
from pydantic import BaseModel, conint

class Limiter(BaseModel):
    max_calls: conint(gt=0) #type: ignore
    period: conint(gt=0) #type: ignore

    _semaphore: Semaphore

    class Config:
        arbitrary_types_allowed=True
        allow_mutation=False
        underscore_attrs_are_private=True

    def __init__(self, **data):
        super().__init__(**data)

        self._semaphore = Semaphore(self.max_calls)

    async def __aenter__ (self):
        await self._semaphore.acquire()
        return
    
    async def __aexit__ (self, exc_type, exc, tb):
        await sleep(self.period)
        self._semaphore.release()
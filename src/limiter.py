from contextlib import asynccontextmanager
from asyncio import Semaphore, sleep
from pydantic import BaseModel, conint

class Limiter(BaseModel):
    max_calls: conint(gt=0) #type: ignore
    period: conint(gt=0) #type: ignore

    class Config:
        arbitrary_types_allowed=True
        allow_mutation=False

    


# @asynccontextmanager
# async def Limiter(semaphore: Semaphore, period: int):
#     async with semaphore:
#         try:
#             yield
#         finally:
#             await sleep(period)
            
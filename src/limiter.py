from contextlib import asynccontextmanager
from asyncio import Semaphore, sleep

@asynccontextmanager
async def Limiter(semaphore: Semaphore, period: int):
    async with semaphore:
        try:
            yield
        finally:
            await sleep(period)
            
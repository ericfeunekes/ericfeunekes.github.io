import asyncio
from asyncio import Semaphore
from datetime import datetime
import numpy as np
import pytest

from src.limiter import Limiter

@pytest.mark.asyncio
async def test_init_limiter():
    num_calls = 4
    sem = Semaphore(num_calls)
    call_times = []
    async def mark_time(i: int, limiter: Limiter):
        async with limiter:
            return {'call':i, 'time':datetime.utcnow()}
    
    tasks = [mark_time(i, Limiter(sem, 2)) for i in range(8)]
    times = await asyncio.gather(*tasks)

    first_batch = [t['time'].second for t in times[:num_calls]]
    first_val = first_batch[0]
    np.testing.assert_equal(first_batch, [first_val]*num_calls)
    second_batch = [t['time'].second for t in times[num_calls:]]
    second_val = second_batch[0]
    np.testing.assert_equal(second_batch, [second_val]*num_calls)

import asyncio
from datetime import datetime
import numpy as np
import pytest

from src.limiter import Limiter

def test_init_limiter():
    print('start')
    limiter = Limiter(max_calls=3, period=1)
    assert limiter.max_calls == 3
    assert limiter.period == 1
    assert limiter._semaphore is not None

@pytest.mark.asyncio
async def test_limiter():
    num_calls = 4
    limiter = Limiter(max_calls=num_calls, period=2)
    call_times = []

    async def mark_time(i: int, limiter: Limiter):
        async with limiter:
            return {"call": i, "time": datetime.utcnow()}

    tasks = [mark_time(i, limiter) for i in range(8)]
    times = await asyncio.gather(*tasks)

    first_batch = [t["time"].second for t in times[:num_calls]]
    first_val = first_batch[0]
    np.testing.assert_equal(first_batch, [first_val] * num_calls)
    second_batch = [t["time"].second for t in times[num_calls:]]
    second_val = second_batch[0]
    np.testing.assert_equal(second_batch, [second_val] * num_calls)

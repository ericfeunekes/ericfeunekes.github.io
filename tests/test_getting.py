import asyncio
from time import time_ns
import httpx
import numpy as np
import pytest
from hypothesis import given, settings
from hypothesis.strategies import integers

from src.getting import get_response, get_url


class TestGet_URL:
    @pytest.mark.asyncio
    @settings(deadline=10000, max_examples=10)
    @given(integers(min_value=200, max_value=299))
    async def test_successful_status_codes(self, code: int):
        """GIVEN status codes in the 200 range, don't raise an error"""
        url = f"https://httpbin.org/status/{code}"
        async with httpx.AsyncClient() as client:
            response = await get_url(url, client)

        assert response.status_code == code

    @pytest.mark.asyncio
    @settings(deadline=10000, max_examples=50)
    @given(integers(min_value=300))
    async def test_failed_status_codes(self, code: int):
        """GIVEN status codes in the greater than 299 (exclude 429), raise an error"""
        sem = asyncio.Semaphore(3)
        url = f"https://httpbin.org/status/{code}"
        async with httpx.AsyncClient() as client:
            with pytest.raises(httpx.HTTPStatusError):
                await get_url(url, client, limiter=sem)

    @pytest.mark.asyncio
    async def test_semaphore_limit(self):
        """GIVEN a semaphore, there should be no more than that number of simultaneous calls"""
        sem = asyncio.Semaphore(3)
        url = f"https://httpbin.org/delay/1"

        times = []

        async def time_calls(client):
            start = time_ns()
            await get_url(url, client, limiter=sem)
            end = time_ns()
            return [start, end]

        async with httpx.AsyncClient() as client:
            todo = [time_calls(client) for i in range(10)]
            times = asyncio.gather(*todo)
        times_np = np.array(times)
        num_calls = [
            len(
                (
                    times_np[
                        (times_np[:, 0] > times_np[i, 0])
                        & (times_np[:, 1] < times_np[i, 1])
                    ]
                )
            )
            for i in range(len(times_np))
        ]
        assert np.max(num_calls) == 3


class TestGetResponse:
    @pytest.mark.asyncio
    @settings(deadline=1000, max_examples=20)
    @given(retries = integers(max_value=15))
    async def test_429_error(self, retries):
        count_tries = 0
        async def mock_getter():
            nonlocal count_tries
            count_tries += 1
            async with httpx.AsyncClient() as client:
                resp = await client.get("http://httpbin.org/status/429")
            resp.raise_for_status()
        with pytest.raises(httpx.HTTPError):
            await get_response(getter=mock_getter, getter_args={}, retries=retries)
        # A negative retry value just means don't retry
        retries = 0 if retries < 0 else retries
        # Takeaway one to account for the first try
        assert count_tries - 1 == retries

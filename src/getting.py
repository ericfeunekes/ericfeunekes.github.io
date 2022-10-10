import httpx
import asyncio

async def get_url(
    url: str, client: httpx.AsyncClient, limiter: asyncio.Semaphore = None
):
    if not limiter:
        return await client.get(url)
    async with limiter:
        return await client.get(url)

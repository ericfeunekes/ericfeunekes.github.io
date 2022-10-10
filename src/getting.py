from typing import Tuple
import httpx
import asyncio


async def get_url(
    url: str, client: httpx.AsyncClient, limiter: asyncio.Semaphore = None
) -> httpx.Response:
    """Send and async request to the given URL using the client

    Parameters
    ---------
    url : str
        the url to get
    """
    assert isinstance(client, httpx.AsyncClient)
    "`client` must be an httpx.AsyncClient"
    if not limiter:
        response = await client.get(url)
    else:
        async with limiter:
            response = await client.get(url)
    response.raise_for_status()
    return response
        


async def get_response(
    url: str, client: httpx.AsyncClient, limiter: asyncio.Semaphore = None
) -> Tuple[bool, httpx.Response]:
    try:
        get_url(url=url, client=client)
    except httpx.HTTPStatusError:
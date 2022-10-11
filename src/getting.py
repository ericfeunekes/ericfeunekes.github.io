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
    url: str,
    client: httpx.AsyncClient,
    limiter: asyncio.Semaphore = None,
    retries: int = 10,
) -> httpx.Response:

    try:
        response: httpx.Response = await get_url(
            url=url, client=client, limiter=limiter
        )
    except httpx.HTTPStatusError as e:
        code = response.status_code
        if code == 429 or (code >= 100 and code < 200):
            if "try_count" not in locals():
                try_count = 1
            else:
                try_count += 1
            if try_count >= retries and retries >= 0:
                print("Max retries exceeded for 429 error")
                raise e
            response = await get_response(
                url=url, client=client, limiter=limiter, retries=retries
            )
        else:
            raise e
        # TODO: account for other error codes; e.g. redirections
    return response

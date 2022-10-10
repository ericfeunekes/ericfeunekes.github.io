from typing import Tuple
import httpx
import asyncio

async def get_url(
    url: str, client: httpx.AsyncClient, limiter: asyncio.Semaphore = None
) -> httpx.Response:
    '''Send and async request to the given URL using the client
    
    :param url: the url to get
    :type url: str
    :param client: the HTTPX async client to use
    :type client: httpx.AsyncClient
    :param limiter: a semaphore to use to limit parallel calls
    :type limiter: asyncio.Semaphore, optional 
    '''
    assert isinstance(client, httpx.AsyncClient); '`client` must be an httpx.AsyncClient'
    if not limiter:
        return await client.get(url)
    async with limiter:
        return await client.get(url)

async def get_response(response: httpx.Response, repeat:int=0) -> Tuple[bool, httpx.Response]:
    code = response.status_code
    match code:
        case 200:
            return (True, response)
        case 429:
            get_url


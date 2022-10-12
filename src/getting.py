from typing import Callable, Tuple, TypedDict
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

class GetterArgs(TypedDict):
    url: str
    client: httpx.AsyncClient
    limiter: asyncio.Semaphore | None
    
async def get_response(
    getter: Callable,
    getter_args: GetterArgs,
    retries: int = 10,
    current_try: int = 0
) -> httpx.Response:
    '''Handles errors that are returned from `get_url`
    
    Parameters
    ----------
    getter : Callable
        the function to use to get the data
    getter_args : GetterArgs
        the arguments to be passed to `get_url`
    retries : int
        the number of times to retry a call, for calls that should be retried

    Returns
    -------
    httpx.Response
        the response from the url
    '''
    try:
        response: httpx.Response = await getter(**getter_args)
    except httpx.HTTPStatusError as e:
        code = e.response.status_code
        if code == 429 or (code >= 100 and code < 200):
            if current_try >= retries or retries <= 0:
                print("Max retries exceeded for 429 error")
                raise e
            current_try += 1
            response = await get_response(getter=getter, getter_args=getter_args, retries=retries, current_try=current_try)
        else:
            raise e
        # TODO: account for other error codes; e.g. redirections
    return response

import asyncio
import logging

import aiohttp

logger = logging.getLogger(__name__)


async def ping(*, url, timeout):
    async with aiohttp.ClientSession() as session:
        try:
            logger.debug(url)

            async with session.get(url, timeout=timeout) as response:
                logger.debug(response.status)
        except (aiohttp.ClientError, asyncio.TimeoutError) as exc:
            logger.exception(exc)


async def heartbeat(*, url, timeout, delay):
    while True:
        try:
            await ping(url=url, timeout=timeout)
        except asyncio.CancelledError:
            break
        except Exception as exc:
            logger.exception(exc)

        await asyncio.sleep(delay)

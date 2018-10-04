import asyncio
import logging

import aiohttp

logger = logging.getLogger(__name__)


async def ping(*, url, timeout):
    async with aiohttp.ClientSession() as session:
        try:
            msg = 'Loading %(url)s'
            context = {'url': url}
            logger.debug(msg, context)

            async with session.get(url, timeout=timeout) as response:
                msg = 'Loaded %(url)s > %(status)d'
                context = {
                    'url': url,
                    'status': response.status,
                }
                logger.debug(msg, context)
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

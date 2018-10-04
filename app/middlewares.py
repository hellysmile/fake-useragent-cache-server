from aiohttp import web

from . import settings


@web.middleware
async def blacklist_middleware(request, handler):
    if request.remote in settings.BLACKLIST:
        raise web.HTTPTooManyRequests

    return await handler(request)

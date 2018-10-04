import asyncio
import logging

import uvloop
from aiohttp import web

from . import settings
from .handlers import Handler
from .heartbeat import heartbeat
from .routes import setup_routes


async def heartbeat_ctx(app):
    loop = asyncio.get_event_loop()

    task = loop.create_task(heartbeat(
        url=settings.HEARTBEAT_URL,
        timeout=settings.HEARTBEAT_TIMEOUT,
        delay=settings.HEARTBEAT_DELAY,
    ))

    yield

    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


def make_app():
    handler = Handler()
    handler.load_data(path=settings.PROJECT_ROOT / 'data')

    app = web.Application()

    setup_routes(app, handler)

    app.cleanup_ctx.append(heartbeat_ctx)

    return app


def main():
    logging.basicConfig(level=logging.DEBUG)

    asyncio.set_event_loop(None)
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    asyncio.set_event_loop(asyncio.new_event_loop())

    app = make_app()

    web.run_app(app, host=settings.HOST, port=settings.PORT)

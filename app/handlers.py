import json
import logging

from aiohttp import web

logger = logging.getLogger(__name__)


class Handler:

    def __init__(self):
        self.files = {}

    def load_data(self, *, path):
        msg = 'Logging for data in %(path)s'
        context = {'path': path}
        logger.debug(msg, context)

        for f in path.glob('*.json'):
            with f.open(mode='rt', encoding='utf-8') as fp:
                self.files[f.namebase] = json.dumps(
                    json.load(fp),
                ).encode('utf-8')

                msg = 'Found %(name)s'
                context = {'name': f.name}
                logger.debug(msg, context)

    async def browsers(self, request):
        version = request.match_info['version']

        if version not in self.files:
            raise web.HTTPNotFound(
                text='No data was found for version {version}'.format(
                    version=version,
                ),
            )

        return web.json_response(body=self.files[version])

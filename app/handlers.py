import io
import json
import os

from aiohttp import web


class Handler:

    def __init__(self):
        self.files = {}

    def load_data(self, *, path):
        for f in path.glob('*.json'):
            with f.open(mode='rt', encoding='utf-8') as fp:
                self.files[f.name] = json.dumps(json.load(fp)).encode('utf-8')

    def browsers(self, request):
        version = request.match_info['version']

        if version not in self.files:
            raise web.HTTPNotFound(
                text='No data was found for version {version}'.format(
                    version=version,
                ),
            )

        return web.json_response(body=self.files[version])

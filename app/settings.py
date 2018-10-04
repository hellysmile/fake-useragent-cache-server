import os

from path import Path
from yarl import URL

PROJECT_ROOT = Path(__file__).abspath().parent

HEARTBEAT_URL = URL('https://fake-useragent.herokuapp.com/')
HEARTBEAT_TIMEOUT = 20
HEARTBEAT_DELAY = 10

HOST = '0.0.0.0'
PORT = os.environ.get('PORT', 8000)

import logging
import asyncio

import aiopg
import psycopg2.extras

import api_hour
from api_hour.utils import get_config

from . import endpoints


LOG = logging.getLogger(__name__)


class Application(api_hour.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # routes
        self.add_url(['GET', 'POST'], '/{{cookiecutter.endpoint_name}}', endpoints.{{cookiecutter.endpoint_name}}.{{cookiecutter.endpoint_name}})

    @asyncio.coroutine
    def start(self):
        yield from super().start()
        # Add your custom start here, example with PostgreSQL:
        self.engines['pg'] = yield from aiopg.create_pool(host=self.config['engines']['pg']['host'],
                                                          port=int(self.config['engines']['pg']['port']),
                                                          dbname=self.config['engines']['pg']['dbname'],
                                                          user=self.config['engines']['pg']['user'],
                                                          password=self.config['engines']['pg']['password'],
                                                          cursor_factory=psycopg2.extras.RealDictCursor,
                                                          minsize=int(self.config['engines']['pg']['minsize']),
                                                          maxsize=int(self.config['engines']['pg']['maxsize']))


    def stop(self):
        # Add your custom end here, example with PostgreSQL:
        if 'pg' in self.engines:
            self.stores['pg'].clear()
        super().stop()

def main(cli_args):
    loop = asyncio.get_event_loop()

    config = get_config(vars(cli_args))
    application = Application(config=config, loop=loop)
    arbiter = api_hour.Arbiter(config=config, application=application, loop=loop)
    arbiter.start()
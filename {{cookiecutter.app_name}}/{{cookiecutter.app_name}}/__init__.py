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
        LOG.info('Starting engines...')
        # Add your custom engine here, example with PostgreSQL:
        self.engines['pg'] = self.loop.create_task(aiopg.create_pool(host=self.config['engines']['pg']['host'],
                                                                     port=int(self.config['engines']['pg']['port']),
                                                                     dbname=self.config['engines']['pg']['dbname'],
                                                                     user=self.config['engines']['pg']['user'],
                                                                     password=self.config['engines']['pg']['password'],
                                                                     cursor_factory=psycopg2.extras.RealDictCursor,
                                                                     minsize=int(self.config['engines']['pg']['minsize']),
                                                                     maxsize=int(self.config['engines']['pg']['maxsize'])))
        yield from asyncio.wait(self.engines.values(), return_when=asyncio.ALL_COMPLETED)

        LOG.info('All engines ready !')


    @asyncio.coroutine
    def stop(self):
        LOG.info('Stopping engines...')
        # Add your custom end here, example with PostgreSQL:
        if 'pg' in self.engines:
            if self.engines['pg'].done():
                self.engines['pg'].result().terminate()
                yield from self.engines['pg'].result().wait_closed()
            else:
                yield from self.engines['pg'].cancel()
        LOG.info('All engines stopped !')
        yield from super().stop()

def main(cli_args):
    loop = asyncio.get_event_loop()

    config = get_config(vars(cli_args))
    application = Application(config=config, loop=loop)
    arbiter = api_hour.Arbiter(config=config, application=application, loop=loop)
    arbiter.start()
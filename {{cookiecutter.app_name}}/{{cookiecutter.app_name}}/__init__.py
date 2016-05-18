import logging
import asyncio

import aiohttp.web
import aiopg
import psycopg2.extras

import api_hour

from . import endpoints


LOG = logging.getLogger(__name__)


class Container(api_hour.Container):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.config is None: # Remove this line if you don't want to use API-Hour config file
            raise ValueError('An API-Hour config dir is needed.')

        ## Servers
        # You can define several servers, to listen HTTP and SSH for example.
        # If you do that, you need to listen on two ports with api_hour --bind command line.
        self.servers['http'] = aiohttp.web.Application(loop=kwargs['loop'])
        self.servers['http']['ah_container'] = self  # keep a reference to Container
        # routes
        self.servers['http'].router.add_route('GET',
                                              '/{{cookiecutter.endpoint_name}}',
                                              endpoints.{{cookiecutter.endpoint_name}}.{{cookiecutter.endpoint_name}})

    async def make_servers(self, sockets):
        # This coroutine is used by api_hour command line to have the list of handlers
        handlers = {}
        handler = self.servers['http'].make_handler(logger=self.worker.log,
                                                    keep_alive=self.worker.cfg.keepalive,
                                                    access_log=self.worker.log.access_log)
        for sock in sockets:
            srv = await self.loop.create_server(handler, sock=sock.sock)
            handlers[srv] = handler
        return handlers

    async def start(self):
        await super().start()
        LOG.info('Starting engines...')
        # Add your custom engines here, example with PostgreSQL:
        self.engines['pg'] = self.loop.create_task(aiopg.create_pool(host=self.config['engines']['pg']['host'],
                                                                     port=int(self.config['engines']['pg']['port']),
                                                                     sslmode='disable',
                                                                     dbname=self.config['engines']['pg']['dbname'],
                                                                     user=self.config['engines']['pg']['user'],
                                                                     password=self.config['engines']['pg']['password'],
                                                                     cursor_factory=psycopg2.extras.RealDictCursor,
                                                                     minsize=int(self.config['engines']['pg']['minsize']),
                                                                     maxsize=int(self.config['engines']['pg']['maxsize']),
                                                                     loop=self.loop))
        await asyncio.wait([self.engines['pg']], return_when=asyncio.ALL_COMPLETED)

        LOG.info('All engines ready !')


    async def stop(self):
        LOG.info('Stopping engines...')
        # Add your custom end here, example with PostgreSQL:
        if 'pg' in self.engines:
            if self.engines['pg'].done():
                self.engines['pg'].result().terminate()
                await self.engines['pg'].result().wait_closed()
            else:
                await self.engines['pg'].cancel()
        LOG.info('All engines stopped !')
        await super().stop()
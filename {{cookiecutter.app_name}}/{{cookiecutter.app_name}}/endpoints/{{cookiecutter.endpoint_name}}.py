from pprint import pprint
import logging
import asyncio

from api_hour.plugins.aiohttp import JSON


LOG = logging.getLogger(__name__)

"""
You handle inputs with outside world here
"""

@asyncio.coroutine
def {{cookiecutter.endpoint_name}}(request):
    return JSON({
        'index': 'hello!'
    })

# Endpoint example with a Service

# from ..services.{{cookiecutter.service_name}} import get_random_record
#
# @asyncio.coroutine
# def db(request):
#     """Test type 2: Single database query"""
#     container = request.app['ah_container']
#
#     return JSON((yield from get_random_record(container)))
#

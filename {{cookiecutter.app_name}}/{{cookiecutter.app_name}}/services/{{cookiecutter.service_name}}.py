import asyncio
from random import randint

"""
You can add your business logic here
"""

async def get_random_record(container):
    pg = await container.engines['pg']

    with (await pg.cursor()) as cur:
        await cur.execute('SELECT id AS "Id", randomnumber AS "RandomNumber" FROM world WHERE id=%(idx)s LIMIT 1',
                               {'idx': randint(1, 10000)})
        world = await cur.fetchone()
    return world

import asyncio
from random import randint

# You can add your business logic here

@asyncio.coroutine
def get_random_record(container):
    pg = yield from container.engines['pg']

    with (yield from pg.cursor()) as cur:
        yield from cur.execute('SELECT id AS "Id", randomnumber AS "RandomNumber" FROM world WHERE id=%(idx)s LIMIT 1',
                               {'idx': randint(1, 10000)})
        world = yield from cur.fetchone()
    return world

import logging
from math import trunc
from random import random
from array import array

# import redis.asyncio as redis
# from sanic import Sanic
# from tinydb import TinyDB, where

from numba import njit


logger = logging.getLogger(__name__)
# db = TinyDB('data.json', indent=4)

# @njit

async def evc2(A, user_id):
    engraved = set()
    logger.info("starting")
    # grid_x = array('l', [0] * res * res)
    # grid_y = array('l', [0] * res * res)
    async def view():
        # grid_cells = []
        html_list = ['''
<body class="gc">
<form data-on:submit="@post('/solve')">
<input id="user-input" type="text" required placeholder="your input here" data-bind:input>
</form>
<div id="plate" style="grid-template-rows: repeat(1000, 4px); grid-template-columns: repeat(1000, 4px);">
'''
        ]
        for y in range(A[1], A[1] + 1001):
            for x in range(A[0], A[0] + 1001):
                if (x, y) in engraved:
                    html_list.append(f'<div class="cell" engraved></div>')
                else:
                    html_list.append(f'<div class="cell"></div>')
        # for n in range(res * res):
            # if grid_x[n] and grid_y[n]:
                # grid_cells.append(f'<div class="cell"></div>')
                # engraved = "engraved"
                # point = [A[0] + 10*j, A[1] + 10*i]
                # is_engraved = "engraved" if point in values else ""
                # is_engraved = "engraved" if random() > .5 else ""
        # grid_html = "".join(grid_cells)
        html_list.append('''</div></body>''')
        html = "".join(html_list)
        logger.info(f"got html {engraved}")
        return html

    def mult(x, y):
        return [x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0]]

    def div(x, y):
        return [trunc(x[0] / y[0]), trunc(x[1] / y[1])]

    def engrave_point(point):
        px, py = point
        zx, zy = 0, 0
        for _ in range(100):
            x2 = zx * zx - zy * zy
            y2 = 2 * zx * zy
            zx = int(x2 / 100_000) + px
            zy = int(y2 / 100_000) + py
            if -1_000_000 <= zx <= 1_000_000 and -1_000_000 <= zy <= 1_000_000:
                continue
            return False
        return True

    # values = []
    html_view = await view()
    yield html_view  # first render:
    # db.update({'html': html_view}, where("user_id") == user_id)
    # logger.info("done")
    # app.ctx.db[user_id] = html_view
    # await app.ctx.redis_client.publish(f"{user_id}", html_view)

    for y in range(A[1], A[1] + 1001):
        for x in range(A[0], A[0] + 1001):
            logger.info(point)
            if engrave_point((x, y)):
                logger.info("got him", point)
                engraved.add(point)
                html_view = await view()
                yield html_view
    # for dx in range(res + 1):
        # for dy in range(res + 1):
    # for n in range(res * res):
        # dx, dy = n % res, n // res
            # # continue
        # point = [A[0] + 10*dx, A[1] + 10*dy]
        # R = [0, 0]
        # engraved = True
        # for _ in range(100):
            # R = mult(R, R)
            # R = div(R, [100000, 100000])
            # R[0] += point[0]
            # R[1] += point[1]
            # if not (-1000000 <= R[0] <= 1000000 and -1000000 <= R[1] <= 1000000):
                # engraved = False
                # break
        # if engraved:
            # # values.append(point)
            # grid_x[n] = point[0]
            # grid_y[n] = point[1]
            # html_view = await view()
            # yield html_view
                # await app.ctx.redis_client.publish(f"{user_id}", html_view)
                # app.ctx.db[user_id] = html_view
                # app.ctx.db[user_id] = html_view
                # db.update({'html': html_view}, where("user_id") == user_id)

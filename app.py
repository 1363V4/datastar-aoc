import asyncio
import logging
from uuid import uuid4

from sanic import Sanic, html, redirect
from datastar_py import ServerSentEventGenerator as SSE
from datastar_py.sanic import datastar_response


app = Sanic(__name__)
app.static('/static/', './static/')
app.static('/', './index.html', name="index")

logging.basicConfig(filename='perso.log', encoding='utf-8', level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    app.run(
    # debug=True,
    debug=False,
    auto_reload=True,
    unix='aoc.sock',
    access_log=False)

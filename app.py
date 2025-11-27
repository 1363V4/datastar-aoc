import asyncio
import logging
from uuid import uuid4

from sanic import Sanic, html, redirect, text
from datastar_py import ServerSentEventGenerator as SSE
from datastar_py.sanic import datastar_response

# import redis.asyncio as redis, meh
# from tinydb import TinyDB, where / PTAIN je pouvais open hidden depuis le deb jsuis trop con

from solvers import evc2


app = Sanic(__name__)
app.static('/static/', './static/')
app.static('/', './index.html', name="index")

logging.basicConfig(filename='perso.log', encoding='utf-8', level=logging.INFO)
logger = logging.getLogger(__name__)

# @app.before_server_start
# async def server_start(app):
    # app.ctx.db = TinyDB('data.json', indent=4)
    # app.ctx.db = {'test': "ok"}
    # app.ctx.redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

@app.on_response
async def cookie(request, response):
    if not request.cookies.get("user_id"):
        user_id = uuid4().hex
        response.add_cookie('user_id', user_id)
        # app.ctx.db.insert({'user_id': user_id, 'html': ""})

@app.get("/<xxc>/<pb>")
async def input_page(request, xxc, pb):
    match xxc, pb:
        case "evc", "25D2":
            return html(open("input.html").read())
        case _:
            return html("404 Not Found")

@app.post("/solve")
@datastar_response
async def solve(request):
    logger.info("solve")
    user_id = request.cookies.get('user_id')
    A = request.json.get('input')
    # A = "A=[35300,-64910]" #debug
    try:
        assert user_id
        A = A.split("=")[1]
        A = A.strip()
        A = A.strip("[]")
        A = A.split(",")
        A = [int(x) for x in A]
        assert isinstance(A, list)
        assert len(A) == 2
        assert all(isinstance(i, int) for i in A)

        async for html in evc2(A, user_id, res=100):
            if html:
                yield SSE.patch_elements(html, mode="replace")
    except (asyncio.CancelledError, GeneratorExit):
        pass
    except Exception as e:
        logger.info(e)
        yield SSE.patch_elements("<body>block</body>")


if __name__ == "__main__":
    app.run(
    # debug=True,
    debug=False,
    auto_reload=True,
    unix='aoc.sock',
    access_log=False)

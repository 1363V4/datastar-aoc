import asyncio
import logging
from uuid import uuid4

from sanic import Sanic, html, redirect, text
from datastar_py import ServerSentEventGenerator as SSE
from datastar_py.sanic import datastar_response

from solvers import evc2


app = Sanic(__name__)
app.static('/static/', './static/')
app.static('/', './index.html', name="index")

logging.basicConfig(filename='perso.log', encoding='utf-8', level=logging.INFO)
logger = logging.getLogger(__name__)

@app.before_server_start
async def open_connections(app):
    app.ctx.db = {'bot': "nope"}

@app.on_response
async def cookie(request, response):
    if not request.cookies.get("user_id"):
        user_id = uuid4().hex

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
    A = request.json.get('input')
    logger.debug(A)
    try:
        A = A.split("=")[1]
        A = A.strip()
        A = A.strip("[]")
        A = A.split(",")
        A = [int(x) for x in A]
        assert isinstance(A, list)
        assert len(A) == 2
        assert all(isinstance(i, int) for i in A)

    # user_input = [-21713,-68997]
        grid_cells = []
        for i in range(100):
            for j in range(100):
                grid_cells.append(
                    f'<div id="{A[0] + j}_{A[1] + i}" class="cell"></div>'
                )
        grid_html = "".join(grid_cells)
        html = f'''
<body class="gc">
<form data-on:submit="@post('/solve')">
<input id="user-input" type="text" required placeholder="your input here" data-bind:input>
</form>
<div id="plate">
{grid_html}
</div>
</body>
'''
        yield SSE.patch_elements(html)
        async for value in evc2(A):
            # html = f'''<div id={"_".join(value)} engraved></div>'''
            logger.debug(value)
            # html = ""
            # yield SSE.patch_elements(html)
        yield
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

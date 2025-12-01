import asyncio
import hashlib
import logging
import platform
from uuid import uuid4

from sanic import Sanic, html
from datastar_py import ServerSentEventGenerator as SSE
from datastar_py.sanic import datastar_response

from solvers import evc25d2, aoc25d1


app = Sanic(__name__)
app.static('/static/', './static/')
app.static('/', './index.html', name="index")

logging.basicConfig(filename='perso.log', encoding='utf-8', level=logging.INFO)
logger = logging.getLogger(__name__)


@app.before_server_start
async def server_start(app):
    app.ctx.cache = {}

@app.on_response
async def cookie(request, response):
    if not request.cookies.get("user_id"):
        user_id = uuid4().hex
        response.add_cookie('user_id', user_id)

PROBLEMS = {
    ("evc", "25D2"): {
        "name": "EVC 25 Day 2",
        "url": "https://everybody.codes/event/2025/quests/2",
        "placeholder": "A=[25,9]"
    },
    ("aoc", "25D1"): {
        "name": "AOC 25 Day 1",
        "url": "https://adventofcode.com/2025/day/1",
        "placeholder": "L68 L30 R48 L5 R60 L55 L1 L99 R14 L82"
    },
    ("evc", "25D10"): {
        "name": "EVC 25 Day 10",
        "url": "https://everybody.codes/event/2025/quests/10",
        "placeholder": "SSS\n..#\n#.#\n#D."
    }
}


@app.get("/<xxc>/<pb>")
async def input_page(request, xxc, pb):
    problem_key = (xxc, pb)
    if problem_key not in PROBLEMS:
        return html("404 Not Found")

    problem = PROBLEMS[problem_key]
    template = open("input.html").read()

    template = template.replace("{{PROBLEM_NAME}}", problem["name"])
    template = template.replace("{{PROBLEM_URL}}", problem["url"])
    template = template.replace("{{PROBLEM_ID}}", f"{xxc}/{pb}")
    template = template.replace("{{INPUT_PLACEHOLDER}}", problem["placeholder"])

    return html(template)


def get_input_hash(input_data):
    return hashlib.md5(str(input_data).encode()).hexdigest()


@app.post("/solve")
@datastar_response
async def solve(request):
    user_id = request.cookies.get('user_id')
    problem_id = request.json.get('problem_id')
    input_data = request.json.get('input')

    try:
        assert user_id
        assert input_data

        cache_key = get_input_hash(f"{problem_id}:{input_data}")
        if cache_key in app.ctx.cache:
            cached_result = app.ctx.cache[cache_key]
            for html_chunk in cached_result:
                yield SSE.patch_elements(html_chunk)
                await asyncio.sleep(.001)
            return

        solver_func = None
        parsed_input = None

        match problem_id:
            case "evc/25D2":
                A = input_data.split("=")[1]
                A = A.strip()
                A = A.strip("[]")
                A = A.split(",")
                A = [int(x) for x in A]
                assert isinstance(A, list)
                assert len(A) == 2
                assert all(isinstance(i, int) for i in A)
                parsed_input = A
                solver_func = evc25d2
            case "aoc/25D1":
                L = [line.strip() for line in input_data.split(" ")]
                L = [(line[0], int(line[1:])) for line in L]
                assert all(line[0] in "LR" for line in L)
                assert all(line[1] < 1000 for line in L)
                parsed_input = L
                solver_func = aoc25d1
            case _:
                pass

        if not solver_func:
            yield SSE.patch_elements("<body>block</body>")
            return

        cached_result = []
        async for html_chunk in solver_func(parsed_input):
            logger.info(html_chunk)
            if html_chunk:
                cached_result.append(html_chunk)
                yield SSE.patch_elements(html_chunk)
            await asyncio.sleep(2)
        app.ctx.cache[cache_key] = cached_result
        logger.info("Another good solve sir :)")

    except (asyncio.CancelledError, GeneratorExit):
        pass
    except Exception as e:
        logger.info(e)
        yield SSE.patch_elements("<body>block</body>")


if __name__ == "__main__":
    is_windows = platform.system() == "Windows"
    app.run(
    debug=is_windows,
    auto_reload=True,
    unix='aoc.sock' if not is_windows else None,
    access_log=False
    )

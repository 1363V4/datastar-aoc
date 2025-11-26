import logging
from math import trunc
from random import random

logger = logging.getLogger(__name__)

async def evc2(A, res=100):
    logger.info("meh")
    async def view(values):
        grid_cells = []
        for i in range(res + 1):
            for j in range(res + 1):
                point = [A[0] + 10*j, A[1] + 10*i]
                is_engraved = "engraved" if point in values else ""
                is_engraved = "engraved" if random() > .5 else ""
                grid_cells.append(f'<div class="cell {is_engraved}"></div>')
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
        return html

    def mult(x, y):
        return [x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0]]

    def div(x, y):
        return [trunc(x[0] / y[0]), trunc(x[1] / y[1])]

    values = []
    html_view = await view(values)
    yield html_view  # first render

    for dx in range(res + 1):
        for dy in range(res + 1):
            continue
            point = [A[0] + 10*dx, A[1] + 10*dy]
            R = [0, 0]
            engraved = True
            for _ in range(100):
                R = mult(R, R)
                R = div(R, [100000, 100000])
                R[0] += point[0]
                R[1] += point[1]
                if not (-1000000 <= R[0] <= 1000000 and -1000000 <= R[1] <= 1000000):
                    engraved = False
                    break
            if engraved:
                values.append(point)
                html_view = await view(values)
                yield html_view

import logging
from math import trunc
from array import array


logger = logging.getLogger(__name__)


async def evc2(A, user_id):
    async def view():
        html_list = ['''
<body class="gc">
<form data-on:submit="@post('/solve')">
<input id="user-input" type="text" required placeholder="your input here" data-bind:input>
</form>
<div id="plate" style="grid-template-rows: repeat(100, 4px); grid-template-columns: repeat(100, 4px);">
'''
        ]
        for y in range(A[1], A[1] + 1001, 10):
            for x in range(A[0], A[0] + 1001, 10):
                html_list.append(f'<div id="x{x}y{y}" class="cell"></div>')
        html_list.append('''</div></body>''')
        html = "".join(html_list)
        return html

    def mult(x, y):
        return [x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0]]

    def div(x, y):
        return [trunc(x[0] / y[0]), trunc(x[1] / y[1])]

    html_view = await view()
    yield html_view  # first render:

    for dy in range(101):
        for dx in range(101):
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
                yield f'<div id="x{point[0]}y{point[1]}" class="cell" engraved></div>'

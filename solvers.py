import asyncio
import logging
from array import array


logger = logging.getLogger(__name__)


async def evc25d2(A):
    async def view():
        html_list = ['''
<body class="gc">
<form>
<input id="user-input" type="text" required placeholder="your input here" data-bind:input>
</form>
<div id="plate" style="grid-template-rows: repeat(101, 4px); grid-template-columns: repeat(101, 4px);">
'''
        ]
        for y in range(A[1], A[1] + 1001, 10):
            for x in range(A[0], A[0] + 1001, 10):
                html_list.append(f'<div id="x{x}y{y}" class="cell"></div>')
        html_list.append('''</div></body>''')
        html = "".join(html_list)
        return html

    def add(a,b):
        X1, Y1 = a
        X2, Y2 = b
        return [X1 + X2, Y1 + Y2]

    def mul(a,b):
        X1, Y1 = a
        X2, Y2 = b
        return [(X1 * X2 - Y1 * Y2), (X1 * Y2 + Y1 * X2)]

    def div(a,b):
        X1, Y1 = a
        X2, Y2 = b
        return [int(X1 / X2), int(Y1 / Y2)]

    def is_engraved(point):
        result = [0,0]
        for x in range(100):
            result = mul(result, result)
            result = div(result, [100000,100000])
            result = add(result, point)
            for coord in result:
                if coord > 1000000 or coord < -1000000:
                    return False
        return True

    html_view = await view()
    yield html_view  # first render:

    for dy in range(101):
        for dx in range(101):
            point = (A[0] + 10*dx, A[1] + 10*dy)
            engraved = is_engraved(point)
            if engraved:
                yield f'<div id="x{point[0]}y{point[1]}" class="cell" engraved></div>'

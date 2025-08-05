import asyncio

import flet as ft


async def main(page: ft.Page):
    svg_image = """
<svg width="400" height="400" xmlns="http://www.w3.org/2000/svg">
 <g>
  <ellipse ry="{}" rx="{}" id="svg_1" cy="200" cx="200" stroke="#000" fill="#fff"/>
 </g>
</svg>
"""

    img = ft.Image(src=svg_image.format(0, 0))
    page.add(img)

    for c in range(0, 10):
        for i in range(0, 10):
            img.src = svg_image.format(i * 10, i * 10)
            img.update()
            await asyncio.sleep(0.1)


ft.run(main)

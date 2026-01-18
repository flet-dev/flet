from dataclasses import dataclass, field

import flet as ft

ItemID = ft.IdCounter()

MAX_SHAPES_PER_CAPTURE = 30

colors = [
    ft.Colors.RED,
    ft.Colors.YELLOW,
    ft.Colors.BLUE,
    ft.Colors.GREEN,
    ft.Colors.ORANGE,
    ft.Colors.PURPLE,
    ft.Colors.PINK,
    ft.Colors.LIME,
    ft.Colors.BLACK,
    ft.Colors.WHITE,
]


@ft.observable
@dataclass
class Item:
    x1: float
    y1: float
    x2: float
    y2: float
    color: ft.Colors
    id: int = field(default_factory=ItemID)


@ft.component
def App():
    import flet.canvas as cv

    items, set_items = ft.use_state([])
    _, set_last_pos = ft.use_state(None)
    color, set_color = ft.use_state(ft.Colors.BLACK)

    def pan_start(e: ft.DragStartEvent):
        set_last_pos((e.local_position.x, e.local_position.y))

    async def pan_update(e: ft.DragUpdateEvent):
        def update_last_pos(prev):
            if prev is not None:
                set_items(
                    lambda cur: cur
                    + [
                        Item(
                            prev[0],
                            prev[1],
                            e.local_position.x,
                            e.local_position.y,
                            color=color,
                        )
                    ]
                )
            return (e.local_position.x, e.local_position.y)

        set_last_pos(update_last_pos)

    async def on_updated():
        if len(items) > MAX_SHAPES_PER_CAPTURE:
            await canvas.capture()
            set_items([])

    ft.on_updated(on_updated)

    async def clear_canvas():
        await canvas.clear_capture()
        set_items([])

    canvas = cv.Canvas(
        shapes=[
            cv.Line(
                item.x1,
                item.y1,
                item.x2,
                item.y2,
                paint=ft.Paint(stroke_width=3, color=item.color),
                key=item.id,
            )
            for item in items
        ],
        content=ft.GestureDetector(
            on_pan_start=pan_start,
            on_pan_update=pan_update,
            drag_interval=10,
        ),
        expand=False,
    )

    def color_clicked(e):
        set_color(e.control.bgcolor)

    return ft.Column(
        controls=[
            ft.Button("Clear", on_click=clear_canvas),
            ft.Row(
                controls=[
                    ft.Container(
                        width=25,
                        height=25,
                        border_radius=25,
                        bgcolor=c,
                        border=ft.Border.all(
                            width=3 if c == color else 1,
                            color=ft.Colors.BLACK_12,
                        ),
                        on_click=color_clicked,
                    )
                    for c in colors
                ]
            ),
            ft.Container(
                canvas,
                border=ft.Border.all(2, ft.Colors.BLACK_54),
                border_radius=5,
                bgcolor=ft.Colors.SURFACE_CONTAINER,
                width=500,
                height=500,
            ),
        ]
    )


if __name__ == "__main__":
    ft.run(lambda page: page.render(App))

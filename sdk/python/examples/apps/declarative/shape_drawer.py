from dataclasses import dataclass, field

import flet as ft
from flet import canvas

POINT_RADIUS = 4
PAINT = ft.Paint(
    style=ft.PaintingStyle.STROKE,
    color=ft.Colors.RED,
    stroke_width=2,
)


@dataclass
class Point:
    x: float = 0
    y: float = 0


@dataclass
@ft.observable
class Polygon:
    points: list[Point] = field(default_factory=list)


@dataclass
@ft.observable
class State:
    polygons: list[Polygon] = field(default_factory=list[Polygon])


@ft.component
def PolygonView(polygon: Polygon) -> canvas.Path:
    return canvas.Path(
        elements=[
            canvas.Path.MoveTo(
                point.x,
                point.y,
            )
            if i == 0
            else canvas.Path.LineTo(
                point.x,
                point.y,
            )
            for i, point in enumerate(polygon.points)
        ]
        + [canvas.Path.Close()],
        paint=PAINT,
    )


@ft.component
def App():
    state, _ = ft.use_state(
        State(
            polygons=[
                Polygon([Point(50, 50), Point(150, 50), Point(100, 150)]),
            ]
        )
    )
    # state, _ = ft.use_state(State(polygons=[Polygon()]))

    def handle_tap_down(e: ft.TapEvent):
        # add point to the top polygon
        if e.local_position is not None:
            state.polygons[-1].points.append(
                Point(x=e.local_position.x, y=e.local_position.y)
            )
            if len(state.polygons[-1].points) == 1:
                # add a temporary point to be updated on hover
                state.polygons[-1].points.append(
                    Point(x=e.local_position.x, y=e.local_position.y)
                )

    def handle_hover(e: ft.HoverEvent):
        # update position of the last point in the top polygon
        if e.local_position is not None and len(state.polygons[-1].points) > 0:
            state.polygons[-1].points[-1].x = e.local_position.x
            state.polygons[-1].points[-1].y = e.local_position.y
            state.notify()

    def handle_secondary_tap_down(e: ft.TapEvent):
        # add new polygon
        state.polygons.append(Polygon())

    return ft.GestureDetector(
        on_tap_down=handle_tap_down,
        on_secondary_tap_down=handle_secondary_tap_down,
        on_hover=handle_hover,
        content=ft.Container(
            content=canvas.Canvas(
                width=float("inf"),
                height=float("inf"),
                shapes=[PolygonView(polygon) for polygon in state.polygons],
            ),
            width=500,
            height=500,
            bgcolor=ft.Colors.GREY_300,
            alignment=ft.Alignment.TOP_LEFT,
        ),
    )


ft.run(lambda page: page.render(App))

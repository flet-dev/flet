import math
from dataclasses import dataclass

import flet as ft
import flet.canvas as fc


@dataclass
class AppState:
    strokes: bool

    def toggle_strokes(self):
        self.strokes = not self.strokes


def main(page: ft.Page):
    state = AppState(strokes=False)

    page.add(
        ft.ControlBuilder(
            state,
            lambda state: ft.SafeArea(
                expand=True,
                content=ft.Column(
                    controls=[
                        ft.Button("Toggle strokes", on_click=state.toggle_strokes),
                        fc.Canvas(
                            width=300,
                            height=300,
                            shapes=[
                                fc.Line(
                                    x1=30,
                                    y1=30,
                                    x2=200,
                                    y2=100,
                                    paint=ft.Paint(
                                        color=ft.Colors.BLACK,
                                        stroke_width=3,
                                        stroke_dash_pattern=[4, 4]
                                        if state.strokes
                                        else None,
                                        style=ft.PaintingStyle.STROKE,
                                    ),
                                ),
                                fc.Circle(
                                    x=150,
                                    y=150,
                                    radius=130,
                                    paint=ft.Paint(
                                        color=ft.Colors.BLUE,
                                        stroke_width=4,
                                        stroke_dash_pattern=[4, 4]
                                        if state.strokes
                                        else None,
                                        style=ft.PaintingStyle.STROKE,
                                    ),
                                ),
                                fc.Oval(
                                    x=10,
                                    y=10,
                                    width=240,
                                    height=140,
                                    paint=ft.Paint(
                                        color=ft.Colors.GREEN,
                                        stroke_width=4,
                                        stroke_dash_pattern=[10, 10]
                                        if state.strokes
                                        else None,
                                        style=ft.PaintingStyle.STROKE,
                                    ),
                                ),
                                fc.Arc(
                                    x=20,
                                    y=20,
                                    width=220,
                                    height=220,
                                    start_angle=0,
                                    sweep_angle=math.pi,
                                    paint=ft.Paint(
                                        color=ft.Colors.RED,
                                        stroke_width=4,
                                        stroke_dash_pattern=[7, 7]
                                        if state.strokes
                                        else None,
                                        style=ft.PaintingStyle.STROKE,
                                    ),
                                ),
                                fc.Rect(
                                    x=40,
                                    y=60,
                                    width=60,
                                    height=70,
                                    border_radius=0,
                                    paint=ft.Paint(
                                        color=ft.Colors.RED,
                                        stroke_width=4,
                                        stroke_dash_pattern=[7, 7]
                                        if state.strokes
                                        else None,
                                        style=ft.PaintingStyle.STROKE,
                                    ),
                                ),
                                fc.Arc(
                                    x=50,
                                    y=50,
                                    width=170,
                                    height=140,
                                    start_angle=math.pi * 0.1,
                                    sweep_angle=math.pi * 0.4,
                                    paint=ft.Paint(
                                        color=ft.Colors.YELLOW,
                                        stroke_width=4,
                                        stroke_dash_pattern=[7, 7]
                                        if state.strokes
                                        else None,
                                        style=ft.PaintingStyle.STROKE,
                                    ),
                                    use_center=True,
                                ),
                            ],
                        ),
                    ]
                ),
            ),
            expand=True,
        )
    )


ft.run(main)

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
                ft.Column(
                    [
                        ft.Button("Toggle strokes", on_click=state.toggle_strokes),
                        fc.Canvas(
                            [
                                fc.Line(
                                    30,
                                    30,
                                    200,
                                    100,
                                    ft.Paint(
                                        color=ft.Colors.BLACK,
                                        stroke_width=3,
                                        stroke_dash_pattern=[4, 4]
                                        if state.strokes
                                        else None,
                                        style=ft.PaintingStyle.STROKE,
                                    ),
                                ),
                                fc.Circle(
                                    150,
                                    150,
                                    130,
                                    ft.Paint(
                                        color=ft.Colors.BLUE,
                                        stroke_width=4,
                                        stroke_dash_pattern=[4, 4]
                                        if state.strokes
                                        else None,
                                        style=ft.PaintingStyle.STROKE,
                                    ),
                                ),
                                fc.Oval(
                                    10,
                                    10,
                                    240,
                                    140,
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
                                    20,
                                    20,
                                    220,
                                    220,
                                    0,
                                    math.pi,
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
                                    40,
                                    60,
                                    60,
                                    70,
                                    0,
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
                                    50,
                                    50,
                                    170,
                                    140,
                                    math.pi * 0.1,
                                    math.pi * 0.4,
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
                            width=300,
                            height=300,
                        ),
                    ]
                ),
                expand=True,
            ),
            expand=True,
        )
    )


ft.run(main)

import flet as ft
import flet_charts as fch

MIN_SPEED = 0
MAX_SPEED = 200
SPEED_LIMIT = 130


def main(page: ft.Page):
    def handle_speed_change(e: ft.Event[ft.Slider]):
        speed.value = needle.value = e.control.value
        reading.value = f"{e.control.value:.0f} km/h"

    page.add(
        ft.SafeArea(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Stack(
                        width=320,
                        height=320,
                        alignment=ft.Alignment.BOTTOM_CENTER,
                        controls=[
                            fch.GaugeChart(
                                min_value=MIN_SPEED,
                                max_value=MAX_SPEED,
                                rings_space=6,
                                rings=[
                                    speed := fch.GaugeProgressRing(
                                        value=60,
                                        width=20,
                                        color=ft.Colors.BLUE,
                                        bgcolor=ft.Colors.with_opacity(
                                            0.12, ft.Colors.ON_SURFACE
                                        ),
                                        stroke_cap=ft.StrokeCap.ROUND,
                                    ),
                                    fch.GaugeZonesRing(
                                        width=8,
                                        zones_space=4,
                                        zones=[
                                            fch.GaugeZone(0, 90, ft.Colors.GREEN),
                                            fch.GaugeZone(90, 130, ft.Colors.AMBER),
                                            fch.GaugeZone(130, 200, ft.Colors.RED),
                                        ],
                                    ),
                                ],
                                ticks=fch.GaugeLineTicks(
                                    count=11,
                                    offset=4,
                                    labels=[str(v) for v in range(0, 201, 20)],
                                    label_style=ft.TextStyle(size=12),
                                    label_offset=4,
                                ),
                                markers=[
                                    fch.GaugeMarker(
                                        value=SPEED_LIMIT,
                                        position=fch.GaugeTickPosition.INNER,
                                        offset=12,
                                        length=16,
                                        thickness=3,
                                        color=ft.Colors.RED,
                                        label="Limit",
                                    )
                                ],
                                pointers=[
                                    needle := fch.GaugeNeedlePointer(
                                        value=60, length=100, width=10, tail_length=20
                                    ),
                                    fch.GaugeCirclePointer(
                                        value=0,
                                        radius=10,
                                        color=ft.Colors.SURFACE,
                                        stroke_width=3,
                                        stroke_color=ft.Colors.ON_SURFACE,
                                    ),
                                ],
                            ),
                            reading := ft.Text(
                                "60 km/h", size=24, weight=ft.FontWeight.BOLD
                            ),
                        ],
                    ),
                    ft.Slider(
                        key="speed",
                        width=320,
                        min=MIN_SPEED,
                        max=MAX_SPEED,
                        value=60,
                        on_change=handle_speed_change,
                    ),
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)

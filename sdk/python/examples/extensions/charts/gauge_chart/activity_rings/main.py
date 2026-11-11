import flet as ft
import flet_charts as fch

ACTIVITIES = [
    ("Stand", 75, ft.Colors.CYAN),
    ("Exercise", 60, ft.Colors.LIGHT_GREEN),
    ("Move", 85, ft.Colors.PINK),
]


def main(page: ft.Page):
    def handle_chart_event(e: fch.GaugeChartEvent):
        for index, ring in enumerate(chart.rings):
            color = ACTIVITIES[index][2]
            ring.color = (
                color
                if e.ring_index in (None, index)
                else ft.Colors.with_opacity(0.3, color)
            )
        if e.ring_index is None:
            caption.value = "Hover a ring"
        else:
            name, goal, _ = ACTIVITIES[e.ring_index]
            caption.value = f"{name}: {goal}%"

    page.add(
        ft.SafeArea(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    chart := fch.GaugeChart(
                        width=260,
                        height=260,
                        max_value=100,
                        start_degree_offset=-90,
                        sweep_angle=360,
                        default_ring_width=24,
                        rings_space=4,
                        on_event=handle_chart_event,
                        rings=[
                            fch.GaugeProgressRing(
                                value=value,
                                color=color,
                                bgcolor=ft.Colors.with_opacity(0.15, color),
                                stroke_cap=ft.StrokeCap.ROUND,
                            )
                            for _, value, color in ACTIVITIES
                        ],
                    ),
                    caption := ft.Text("Hover a ring", size=18),
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)

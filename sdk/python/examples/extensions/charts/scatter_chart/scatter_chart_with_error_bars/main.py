import statistics

import flet as ft
import flet_charts as fch

# Five timings of one swing (in seconds) for each pendulum string length (in cm).
TIMINGS = {
    20: [0.84, 0.95, 0.90, 0.88, 0.93],
    40: [1.22, 1.33, 1.27, 1.25, 1.30],
    60: [1.50, 1.62, 1.55, 1.52, 1.58],
    80: [1.73, 1.86, 1.80, 1.76, 1.82],
    100: [1.94, 2.09, 2.00, 1.98, 2.03],
    120: [2.13, 2.29, 2.19, 2.17, 2.24],
}

# How far off each measured string length may be, in cm.
LENGTH_UNCERTAINTY = 3


def main(page: ft.Page):
    grid_color = ft.Colors.with_opacity(0.2, ft.Colors.ON_SURFACE)

    spots = []
    for length, timings in TIMINGS.items():
        mean = statistics.fmean(timings)
        spots.append(
            fch.ScatterChartSpot(
                x=length,
                y=mean,
                radius=6,
                color=ft.Colors.INDIGO,
                tooltip=f"{mean:.2f} s",
                x_error=fch.ChartErrorRange.symmetric(LENGTH_UNCERTAINTY),
                y_error=fch.ChartErrorRange(
                    lower_by=mean - min(timings),
                    upper_by=max(timings) - mean,
                ),
            )
        )

    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Text(
                        "Mean period of a pendulum over five timings. Vertical bars "
                        "span the fastest and slowest timing, horizontal bars the "
                        f"±{LENGTH_UNCERTAINTY} cm uncertainty of the string length."
                    ),
                    fch.ScatterChart(
                        expand=True,
                        min_x=0,
                        max_x=140,
                        min_y=0.5,
                        max_y=2.5,
                        border=ft.Border.all(1, grid_color),
                        horizontal_grid_lines=fch.ChartGridLines(
                            interval=0.5, color=grid_color, width=1
                        ),
                        vertical_grid_lines=fch.ChartGridLines(
                            interval=20, color=grid_color, width=1
                        ),
                        left_axis=fch.ChartAxis(
                            title=ft.Text("Period (s)"),
                            title_size=24,
                            label_spacing=0.5,
                            label_size=40,
                        ),
                        bottom_axis=fch.ChartAxis(
                            title=ft.Text("String length (cm)"),
                            title_size=24,
                            label_spacing=20,
                            label_size=28,
                            show_max=False,
                        ),
                        spots=spots,
                    ),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)

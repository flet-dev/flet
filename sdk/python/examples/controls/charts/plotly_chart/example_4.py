import plotly.graph_objects as go

import flet as ft
import flet_charts as fch


def main(page: ft.Page):
    x = [
        "day 1",
        "day 1",
        "day 1",
        "day 1",
        "day 1",
        "day 1",
        "day 2",
        "day 2",
        "day 2",
        "day 2",
        "day 2",
        "day 2",
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Box(
            y=[0.2, 0.2, 0.6, 1.0, 0.5, 0.4, 0.2, 0.7, 0.9, 0.1, 0.5, 0.3],
            x=x,
            name="kale",
            marker_color="#3D9970",
        )
    )
    fig.add_trace(
        go.Box(
            y=[0.6, 0.7, 0.3, 0.6, 0.0, 0.5, 0.7, 0.9, 0.5, 0.8, 0.7, 0.2],
            x=x,
            name="radishes",
            marker_color="#FF4136",
        )
    )
    fig.add_trace(
        go.Box(
            y=[0.1, 0.3, 0.1, 0.9, 0.6, 0.6, 0.9, 1.0, 0.3, 0.6, 0.8, 0.5],
            x=x,
            name="carrots",
            marker_color="#FF851B",
        )
    )

    fig.update_layout(
        yaxis_title="normalized moisture",
        boxmode="group",  # group together boxes of the different traces
    )

    page.add(fch.PlotlyChart(figure=fig, expand=True))


if __name__ == "__main__":
    ft.run(main)

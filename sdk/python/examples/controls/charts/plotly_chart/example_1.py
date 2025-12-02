import plotly.express as px

import flet as ft
import flet_charts as fch


def main(page: ft.Page):
    df = px.data.gapminder().query("continent=='Oceania'")
    fig = px.line(df, x="year", y="lifeExp", color="country")

    page.add(fch.PlotlyChart(figure=fig, expand=True))


if __name__ == "__main__":
    ft.run(main)

import flet_charts as fch
import plotly.express as px

import flet as ft


def main(page: ft.Page):
    df = px.data.gapminder().query("continent=='Oceania'")
    fig = px.line(df, x="year", y="lifeExp", color="country")

    page.add(fch.PlotlyChart(figure=fig, expand=True))


ft.run(main)

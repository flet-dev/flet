import flet_charts as fch
import plotly.express as px

import flet as ft


def main(page: ft.Page):
    df = px.data.gapminder().query("continent == 'Oceania'")
    fig = px.bar(
        df,
        x="year",
        y="pop",
        hover_data=["lifeExp", "gdpPercap"],
        color="country",
        labels={"pop": "population of Canada"},
        height=400,
    )

    page.add(fch.PlotlyChart(figure=fig, expand=True))


ft.run(main)

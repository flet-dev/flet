import flet as ft
from weather_widget.weather_widget import Weather, WeatherAsync


def main(page: ft.Page):
    weather_widget = Weather()
    weather_widget_async = WeatherAsync()

    page.add(weather_widget)
    page.add(weather_widget_async)


ft.app(main)

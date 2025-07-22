import asyncio
import os
import time

import flet as ft
import geocoder
import httpx
import requests


class Weather(ft.Container):
    def __init__(self, height=200, width=200, bgcolor=ft.Colors.BLUE_200):
        super().__init__()
        self.OWM_Endpoint = "https://api.openweathermap.org/data/2.5/weather"
        self._api_key = os.environ.get("OWM_API_KEY")
        self.height = height
        self.width = width
        self.bgcolor = bgcolor
        self.border_radius = 10
        self.location_text = ft.Text(style=ft.TextStyle(size=15))
        self.description_text = ft.Text(style=ft.TextStyle(size=20))
        self.weather_icon = ft.Image(
            # empty image
            src_base64="iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==",
            height=100,
            width=100,
        )
        self.temp_text = ft.Text(style=ft.TextStyle(size=30))
        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.location_text,
                self.description_text,
                ft.Row([self.weather_icon, self.temp_text]),
            ],
        )

    def get_weather_params(self):
        myloc = geocoder.ip("me")
        self.location_text.value = myloc.city

        return {
            "lat": myloc.latlng[0],
            "lon": myloc.latlng[1],
            "appid": self._api_key,
        }

    def did_mount(self):
        self.running = True
        # update_weather calls sync requests.get() and time.sleep() and therefore has to be run in a separate thread
        self.page.run_thread(self.update_weather)

    def will_unmount(self):
        self.running = False

    def update_weather(self):
        while self.running:
            response = requests.get(self.OWM_Endpoint, params=self.get_weather_params())
            response.raise_for_status()
            weather_data = response.json()

            self.description_text.value = weather_data["weather"][0][
                "description"
            ].capitalize()
            self.temp_text.value = self.display_temp(weather_data["main"]["temp"])
            icon_file = weather_data["weather"][0]["icon"]
            self.weather_icon.src_base64 = None
            self.weather_icon.src = (
                f"https://openweathermap.org/img/wn/{icon_file}@2x.png"
            )
            self.update()
            time.sleep(60)

    def display_temp(self, temp):
        c_temp = round(temp - 273.15)
        return f"{'+' if c_temp > 0 else ''}{c_temp}\N{DEGREE SIGN}C"


class WeatherAsync(ft.Container):
    def __init__(self, height=200, width=200, bgcolor=ft.Colors.BLUE_200):
        super().__init__()
        self.OWM_Endpoint = "https://api.openweathermap.org/data/2.5/weather"
        self._api_key = os.environ.get("OWM_API_KEY")
        self.height = height
        self.width = width
        self.bgcolor = bgcolor
        self.border_radius = 10
        self.location_text = ft.Text(style=ft.TextStyle(size=15))
        self.description_text = ft.Text(style=ft.TextStyle(size=20))
        self.weather_icon = ft.Image(
            # empty image
            src_base64="iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==",
            height=100,
            width=100,
        )
        self.temp_text = ft.Text(style=ft.TextStyle(size=30))
        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.location_text,
                self.description_text,
                ft.Row([self.weather_icon, self.temp_text]),
            ],
        )

    def get_weather_params(self):
        myloc = geocoder.ip("me")
        self.location_text.value = myloc.city

        return {
            "lat": myloc.latlng[0],
            "lon": myloc.latlng[1],
            "appid": self._api_key,
        }

    def did_mount(self):
        self.running = True
        print(self.uid)
        # update_weather uses async httpx and and asyncio.sleep(60) and therefore should be run as async task
        self.page.run_task(self.update_weather)

    def will_unmount(self):
        self.running = False

    async def update_weather(self):
        while self.running:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.OWM_Endpoint, params=self.get_weather_params()
                )
            response.raise_for_status()
            weather_data = response.json()

            self.description_text.value = weather_data["weather"][0][
                "description"
            ].capitalize()
            self.temp_text.value = self.display_temp(weather_data["main"]["temp"])
            icon_file = weather_data["weather"][0]["icon"]
            self.weather_icon.src_base64 = None
            self.weather_icon.src = (
                f"https://openweathermap.org/img/wn/{icon_file}@2x.png"
            )
            self.update()
            await asyncio.sleep(60)

    def display_temp(self, temp):
        c_temp = round(temp - 273.15)
        return f"{'+' if c_temp > 0 else ''}{c_temp}\N{DEGREE SIGN}C"

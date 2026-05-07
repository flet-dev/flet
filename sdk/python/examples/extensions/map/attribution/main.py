import flet as ft
import flet_map as ftm


def main(page: ft.Page):
    def launch_url(url: str):
        page.run_task(ft.UrlLauncher().launch_url, url)

    page.add(
        ft.SafeArea(
            expand=True,
            content=ftm.Map(
                expand=True,
                initial_zoom=11,
                initial_center=ftm.MapLatitudeLongitude(
                    latitude=40.7128, longitude=-74.0060
                ),
                layers=[
                    ftm.TileLayer(
                        url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                        user_agent_package_name="flet-map-examples/1.0",
                        on_image_error=lambda e: print(f"TileLayer Error: {e.data}"),
                    ),
                    ftm.SimpleAttribution(
                        text="OpenStreetMap contributors",
                        text_style=ft.TextStyle(
                            color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=15
                        ),
                        alignment=ft.Alignment.TOP_RIGHT,
                        bgcolor=ft.Colors.BLUE,
                        on_click=lambda: launch_url(
                            "https://www.openstreetmap.org/copyright"
                        ),
                    ),
                    ftm.RichAttribution(
                        alignment=ftm.AttributionAlignment.BOTTOM_RIGHT,
                        popup_bgcolor=ft.Colors.WHITE,
                        popup_border_radius=8,
                        popup_initial_display_duration=4000,
                        permanent_height=28,
                        attributions=[
                            ftm.ImageSourceAttribution(
                                image=ft.Image(
                                    src="iVBORw0KGgoAAAANSUhEUgAAABkAAAAgCAYAAADnnNMGAAAACXBIWXMAAAORAAADkQFnq8zdAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAA6dJREFUSImllltoHFUYx3/fzOzm0lt23ZrQ1AQbtBehNpvQohgkBYVo410RwQctNE3Sh0IfiiBoIAjqi6TYrKnFy4O3oiiRavDJFi3mXomIBmOxNZe63ay52GR3Zj4f2sTEzmx3m//TYf7/c35zvgPnO6KqrESXqpq3muocAikv6m+/zytj3ejik1VN21G31YA9CgJ6xC+bMyQZPVCuarciPAMYC99V6Vw5pLbFSibHmlVoRVj9P3cmPBM8tSJI/M6mzabpfoAQ9fIF7WK4bd5vvuFnLGgy2vi0abg94A0AcJGvMq3hDxGRyar9r4F+iLAm0yIiRk8m37tctS1WsrIhhrI30+Srmg+J87OXUf3lWGS1q89dC6ltsSanxk4Aj2QBABii96300g87P/rtlrWr8l+vyDMfdlXSyyEikqxsiOUAQJCBhfHdXRfCq1LSsSlcWG+KBAGStvvrMkgiuv8lUc2mREukPwLUfHG+uTQv8Eown7VL3XlbBxYhf1c17hbVF3MDwA9bts280TnaU1YYqPby07aeFlUlHt27wSQ4CLo+F8AvoTCvHmyKF+ZbEb/M77P2LgvAwmrTHAHflN3KZxVbMC2jMFNOpgPnrMSOhvvFkMezXdwV4ePbtvHtxnJAMQ0j4JtVnO+eLb5oiSlt5HDbv7t1O90lpYCCCKbhfzW5kAIwUAazR0BlfII8Ow0I6uoVmI9MyAMwbMs8CExmDbk4zgu931MyO4OI4KrYflkRjOoTI+uM9d1vjotwKPu9QMk/sxzuO8POiVFcdZ1M2YBVsMEAKOqLvaPIe7mACuw0z/80SMH58SMplxlfiDhVi7dw2pltRhjKBQTQdrSja2KKTfE551NHuaZ0QVPvWYQUn31/Vm2nDvgjF4grVJx6suSvrvrSJ/6cSW2Oz9mf264uNrB806xZ1k/CZ49dUKgDEtlCROX2hfHpx8pGuuo3PpqYulw8fjndOp1yhgtNKRevJ1FyR2Ola+jXAjdnwTkZ6o896GdWdxDw7IxFg+0DpmXchTKSBWQnIuJn9u4j7dt+13UfHXEkXQOcuQ4kMhVtqsgUyPiQiPQfHw1NB2sRjmXKuTg1NwwBYLhtPtQX26eqTwGXPDOqvmcC4Hnwfrrad94GrVsOYTqUTkQY+iTlNe/6O1miSP/x0VB/+wMIDwHn/vtV1iQC4Xv95uUEWVCoL9Y5Z+gdovoyMHUFJHv88jmVy0vTuw7cZNv2YaA61Bfb7ZX5F8SaUv2xwZevAAAAAElFTkSuQmCC",  # noqa: E501
                                    width=74,
                                    height=28,
                                    fit=ft.BoxFit.CONTAIN,
                                ),
                                height=28,
                                tooltip="Flet Logo",
                                on_click=lambda: launch_url("https://flet.dev"),
                            ),
                            ftm.TextSourceAttribution(
                                text="OpenStreetMap contributors",
                                text_style=ft.TextStyle(size=12),
                                on_click=lambda: launch_url(
                                    "https://www.openstreetmap.org/copyright"
                                ),
                            ),
                            ftm.TextSourceAttribution(
                                text="flet-map",
                                text_style=ft.TextStyle(
                                    color=ft.Colors.RED,
                                    size=15,
                                    weight=ft.FontWeight.BOLD,
                                    decoration=ft.TextDecoration.UNDERLINE,
                                ),
                                prepend_copyright=False,
                                on_click=lambda: launch_url(
                                    "https://flet.dev/docs/controls/map/"
                                ),
                            ),
                        ],
                    ),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)

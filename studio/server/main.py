import logging

import flet as ft

# logging.basicConfig(level=logging.DEBUG)


def main(page: ft.Page):
    hf = ft.HapticFeedback()
    page.overlay.append(hf)
    # page.padding = 0
    page.appbar = ft.AppBar(title=ft.Text("Flet"))

    def return_to_main(_):
        if len(page.views) > 1:
            print("RETURN TO MAIN!")
            hf.heavy_impact()
            page.views.pop()
            page.update()

    shd = ft.ShakeDetector(
        minimum_shake_count=2,
        shake_slop_time_ms=300,
        shake_count_reset_time_ms=1000,
        on_shake=return_to_main,
    )
    page.overlay.append(shd)

    def run_app(url):
        page.views.append(
            ft.View(
                "/",
                controls=[
                    ft.Stack(
                        [
                            ft.GestureDetector(
                                on_tap=lambda _: print("TAP!"),
                                multi_tap_touches=3,
                                on_multi_tap=lambda e: print(
                                    "MULTI TAP:", e.correct_touches
                                ),
                                on_multi_long_press=return_to_main,
                            ),
                            ft.TransparentPointer(ft.FletApp(url=url)),
                        ],
                        expand=True,
                    )
                ],
                padding=0,
            )
        )
        page.update()

    page.add(
        ft.ElevatedButton(
            "Counter app",
            on_click=lambda _: run_app("http://Feodors-MacBook-Pro.local:8560"),
        ),
        ft.ElevatedButton(
            "Flet animation app",
            on_click=lambda _: run_app("http://Feodors-MacBook-Pro.local:8570"),
        ),
    )


ft.app(target=main, port=8550, view=ft.WEB_BROWSER)

import logging

import flet
from flet import (
    AppBar,
    Container,
    ElevatedButton,
    FletApp,
    GestureDetector,
    HapticFeedback,
    Page,
    ShakeDetector,
    Stack,
    Text,
    TransparentPointer,
    colors,
    View,
)

# logging.basicConfig(level=logging.DEBUG)


def main(page: Page):
    hf = HapticFeedback()
    page.overlay.append(hf)
    # page.padding = 0
    page.appbar = AppBar(title=Text("Flet Studio"))

    def return_to_main(_):
        if len(page.views) > 1:
            print("RETURN TO MAIN!")
            hf.heavy_impact()
            page.views.pop()
            page.update()

    shd = ShakeDetector(
        minimum_shake_count=2,
        shake_slop_time_ms=300,
        shake_count_reset_time_ms=1000,
        on_shake=return_to_main,
    )
    page.overlay.append(shd)

    def run_app(url):
        page.views.append(
            View(
                "/",
                controls=[
                    Stack(
                        [
                            GestureDetector(
                                on_tap=lambda _: print("TAP!"),
                                multi_tap_touches=3,
                                on_multi_tap=lambda e: print(
                                    "MULTI TAP:", e.correct_touches
                                ),
                                on_multi_long_press=return_to_main,
                            ),
                            TransparentPointer(FletApp(url=url)),
                        ],
                        expand=True,
                    )
                ],
                padding=0,
            )
        )
        page.update()

    page.add(
        ElevatedButton(
            "Counter app", on_click=lambda _: run_app("http://192.168.1.243:8560")
        ),
        ElevatedButton(
            "Flet animation app",
            on_click=lambda _: run_app("http://192.168.1.243:8570"),
        ),
    )


flet.app(target=main, port=8550, view=flet.WEB_BROWSER)

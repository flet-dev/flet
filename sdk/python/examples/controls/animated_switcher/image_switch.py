import time

import flet as ft


def main(page: ft.Page):
    def animate(e: ft.Event[ft.Button]):
        switcher.content = ft.Image(
            src=f"https://picsum.photos/200/300?{time.time()}",
            width=200,
            height=300,
        )
        page.update()

    page.add(
        switcher := ft.AnimatedSwitcher(
            content=ft.Image(
                src="https://picsum.photos/200/300",
                width=200,
                height=300,
            ),
            transition=ft.AnimatedSwitcherTransition.SCALE,
            duration=500,
            reverse_duration=100,
            switch_in_curve=ft.AnimationCurve.BOUNCE_OUT,
            switch_out_curve=ft.AnimationCurve.BOUNCE_IN,
        ),
        ft.Button("Animate!", on_click=animate),
    )


ft.run(main)

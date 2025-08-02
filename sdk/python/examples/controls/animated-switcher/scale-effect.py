import flet as ft


def main(page: ft.Page):
    c1 = ft.Container(
        content=ft.Text("Hello!", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM),
        alignment=ft.Alignment.CENTER,
        width=200,
        height=200,
        bgcolor=ft.Colors.GREEN,
    )
    c2 = ft.Container(
        content=ft.Text("Bye!", size=50),
        alignment=ft.Alignment.CENTER,
        width=200,
        height=200,
        bgcolor=ft.Colors.YELLOW,
    )
    switcher = ft.AnimatedSwitcher(
        content=c1,
        transition=ft.AnimatedSwitcherTransition.SCALE,
        duration=500,
        reverse_duration=100,
        switch_in_curve=ft.AnimationCurve.BOUNCE_OUT,
        switch_out_curve=ft.AnimationCurve.BOUNCE_IN,
    )

    def scale(e):
        switcher.content = c2 if switcher.content == c1 else c1
        switcher.transition = ft.AnimatedSwitcherTransition.SCALE
        switcher.update()

    def fade(e):
        switcher.content = c2 if switcher.content == c1 else c1
        switcher.transition = ft.AnimatedSwitcherTransition.FADE
        switcher.update()

    def rotate(e):
        switcher.content = c2 if switcher.content == c1 else c1
        switcher.transition = ft.AnimatedSwitcherTransition.ROTATION
        switcher.update()

    page.add(
        switcher,
        ft.ElevatedButton("Scale", on_click=scale),
        ft.ElevatedButton("Fade", on_click=fade),
        ft.ElevatedButton("Rotate", on_click=rotate),
    )


ft.run(main)

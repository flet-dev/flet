import flet as ft

name = "Animated switching between two containers with scale effect"


def example():
    c1 = ft.Container(
        ft.Text("Hello!", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM),
        alignment=ft.Alignment.CENTER,
        width=200,
        height=200,
        bgcolor=ft.Colors.GREEN,
    )
    c2 = ft.Container(
        ft.Text("Bye!", size=50),
        alignment=ft.Alignment.CENTER,
        width=200,
        height=200,
        bgcolor=ft.Colors.YELLOW,
    )
    c = ft.AnimatedSwitcher(
        c1,
        transition=ft.AnimatedSwitcherTransition.SCALE,
        duration=500,
        reverse_duration=100,
        switch_in_curve=ft.AnimationCurve.BOUNCE_OUT,
        switch_out_curve=ft.AnimationCurve.BOUNCE_IN,
    )

    def animate(e):
        c.content = c2 if c.content == c1 else c1
        c.update()

    return ft.Column(controls=[c, ft.ElevatedButton("Animate!", on_click=animate)])

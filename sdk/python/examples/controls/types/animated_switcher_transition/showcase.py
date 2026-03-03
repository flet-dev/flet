import flet as ft


def showcase_card(transition: ft.AnimatedSwitcherTransition) -> ft.Container:
    state = 0
    values = ["A", "B"]

    switcher = ft.AnimatedSwitcher(
        duration=500,
        reverse_duration=300,
        transition=transition,
        content=ft.Text(
            values[0],
            size=40,
            weight=ft.FontWeight.BOLD,
        ),
    )

    def swap(_):
        nonlocal state
        state = 1 - state
        switcher.content = ft.Text(
            values[state],
            size=40,
            weight=ft.FontWeight.BOLD,
        )
        switcher.update()

    return ft.Container(
        width=320,
        padding=12,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(transition.name, weight=ft.FontWeight.BOLD),
                ft.Container(
                    width=240,
                    height=90,
                    border=ft.Border.all(1, ft.Colors.OUTLINE),
                    border_radius=8,
                    bgcolor=ft.Colors.SURFACE,
                    alignment=ft.Alignment.CENTER,
                    content=switcher,
                ),
                ft.Button("Swap", on_click=swap),
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="AnimatedSwitcherTransition Showcase")
    page.add(
        ft.Text("Swap content to compare switcher transition effects."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                showcase_card(transition)
                for transition in ft.AnimatedSwitcherTransition
            ],
        ),
    )


ft.run(main)

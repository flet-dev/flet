import flet as ft


def showcase_card(interaction: ft.SliderInteraction) -> ft.Container:
    value_text = ft.Text("Value: 50")

    def on_change(e: ft.Event[ft.Slider]):
        value_text.value = f"Value: {round(e.control.value)}"
        value_text.update()

    return ft.Container(
        width=340,
        padding=12,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(interaction.name, weight=ft.FontWeight.BOLD),
                value_text,
                ft.Container(
                    width=260,
                    padding=ft.Padding.symmetric(horizontal=8),
                    border=ft.Border.all(1, ft.Colors.OUTLINE),
                    border_radius=8,
                    bgcolor=ft.Colors.SURFACE,
                    content=ft.Slider(
                        min=0,
                        max=100,
                        value=50,
                        divisions=20,
                        interaction=interaction,
                        on_change=on_change,
                    ),
                ),
                ft.Text("Try tapping track and dragging thumb.", size=11),
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="SliderInteraction Showcase")
    page.add(
        ft.Text("Compare which gestures are accepted by each slider mode."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(i) for i in ft.SliderInteraction],
        ),
    )


ft.run(main)

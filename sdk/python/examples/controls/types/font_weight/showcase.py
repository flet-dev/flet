import flet as ft

SAMPLE_TEXT = "Sphinx of black quartz"


def showcase_card(weight: ft.FontWeight) -> ft.Container:
    return ft.Container(
        width=300,
        padding=12,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(weight.name, size=12, color=ft.Colors.ON_SURFACE_VARIANT),
                ft.Text(SAMPLE_TEXT, weight=weight, size=24),
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="FontWeight Showcase")
    page.add(
        ft.Text("Compare text thickness across all FontWeight values."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(weight) for weight in ft.FontWeight],
        ),
    )


ft.run(main)

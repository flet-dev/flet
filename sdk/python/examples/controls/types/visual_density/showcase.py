import flet as ft


def density_card(visual_density: ft.VisualDensity) -> ft.Container:
    return ft.Container(
        width=300,
        padding=12,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        theme=ft.Theme(visual_density=visual_density),
        dark_theme=ft.Theme(visual_density=visual_density),
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(visual_density.name, weight=ft.FontWeight.BOLD),
                ft.IconButton(icon=ft.Icons.ADD),
                ft.Checkbox(label="Checkbox", value=True),
                ft.Chip(
                    label="Explore topics",
                    leading=ft.Icon(ft.Icons.EXPLORE_OUTLINED),
                ),
                ft.RadioGroup(
                    value="1",
                    content=ft.Row(
                        controls=[
                            ft.Radio(label=f"{i}", value=f"{i}") for i in range(1, 4)
                        ],
                    ),
                ),
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="VisualDensity Showcase")
    page.add(
        ft.Text("Compare component density presets across Material controls."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[density_card(vd) for vd in ft.VisualDensity],
        ),
    )


ft.run(main)

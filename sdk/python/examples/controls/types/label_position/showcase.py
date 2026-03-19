import flet as ft


def showcase_card(label_position: ft.LabelPosition) -> ft.Container:
    return ft.Container(
        width=280,
        padding=12,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=10,
            controls=[
                ft.Text(label_position.name, weight=ft.FontWeight.BOLD),
                ft.Checkbox(
                    label="Checkbox label",
                    value=True,
                    label_position=label_position,
                ),
                ft.RadioGroup(
                    content=ft.Row(
                        controls=[
                            ft.Radio(
                                label=f"{i}",
                                value=f"{i}",
                                label_position=label_position,
                            )
                            for i in range(1, 4)
                        ],
                    )
                ),
                ft.Switch(
                    label="Switch label",
                    value=True,
                    label_position=label_position,
                ),
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="LabelPosition Showcase")
    page.add(
        ft.Text("Compare left/right label placement for form controls."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                showcase_card(label_position) for label_position in ft.LabelPosition
            ],
        ),
    )


ft.run(main)

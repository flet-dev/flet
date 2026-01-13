import flet as ft


@ft.component
def GroupCard(
    title: str = "Group Title",
    controls: list | None = None,
    elevation: int = 5,
    margin=None,
    padding: int = 20,
):
    """Reusable card that groups a list of controls with an optional title.

    Args:
        title: Optional title shown at the top of the card.
        controls: A list of `ft.Control` instances to display inside the card.
        elevation: Card elevation.
        margin: Card margin.
        padding: Inner padding for the card content container.
    """
    if margin is None:
        margin = ft.Margin.all(10)
    if controls is None:
        controls = []
    content_controls = []
    if title:
        content_controls.append(
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        title,
                        style=ft.TextStyle(
                            weight=ft.FontWeight.BOLD,
                            size=16,
                            color=ft.Colors.PRIMARY,
                        ),
                    )
                ],
            )
        )
    if controls:
        content_controls.extend(controls)

    return ft.Card(
        content=ft.Container(
            expand=True,
            padding=padding,
            content=ft.Column(controls=content_controls, expand=True),
        ),
        elevation=elevation,
        margin=margin,
        expand=True,
    )


@ft.component
def App():
    return ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        alignment=ft.MainAxisAlignment.START,
        controls=[
            GroupCard(
                title="Input Controls",
                controls=[
                    ft.Checkbox(label="Checkbox"),
                    ft.Switch(label="Switch"),
                    ft.RadioGroup(
                        content=ft.Column(
                            controls=[
                                ft.Radio(label="Radio 1", value="r1"),
                                ft.Radio(label="Radio 2", value="r2"),
                            ]
                        )
                    ),
                    ft.Slider(min=0, max=100, divisions=10, label="{value}"),
                    ft.TextField(label="Text Field"),
                    ft.Dropdown(
                        label="Dropdown",
                        options=[
                            ft.dropdown.Option("Option 1"),
                            ft.dropdown.Option("Option 2"),
                            ft.dropdown.Option("Option 3"),
                        ],
                    ),
                ],
            ),
            GroupCard(
                title="Dialogs",
                controls=[
                    ft.Row(
                        controls=[
                            ft.TextButton(
                                "Show Dialog",
                                on_click=lambda e: e.page.show_dialog(
                                    ft.AlertDialog(
                                        content=ft.Text("Hello from Flet!"),
                                        actions=[
                                            ft.TextButton(
                                                "OK",
                                                on_click=lambda ev: ev.page.pop_dialog(),  # noqa: E501
                                            )
                                        ],
                                    )
                                ),
                            ),
                            ft.TextButton(
                                "Show Banner",
                                on_click=lambda e: e.page.show_dialog(
                                    ft.Banner(
                                        leading=ft.Icon(
                                            ft.Icons.INFO_OUTLINED,
                                            color=ft.Colors.PRIMARY,
                                        ),
                                        content=ft.Text(
                                            "Backup completed successfully."
                                        ),
                                        actions=[
                                            ft.TextButton(
                                                "Dismiss",
                                                on_click=lambda ev: ev.page.pop_dialog(),  # noqa: E501
                                            )
                                        ],
                                        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
                                        open=True,
                                    ),
                                ),
                            ),
                        ],
                    ),
                    ft.Row(
                        controls=[
                            ft.TextButton(
                                "Show DatePicker",
                                on_click=lambda e: e.page.show_dialog(
                                    ft.DatePicker(),
                                ),
                            ),
                            ft.TextButton(
                                "Show TimePicker",
                                on_click=lambda e: e.page.show_dialog(
                                    ft.TimePicker(),
                                ),
                            ),
                        ],
                    ),
                ],
            ),
            GroupCard(
                title="Buttons",
                controls=[
                    ft.Row(
                        [
                            ft.Button(
                                content="Button",
                                expand=1,
                            ),
                            ft.Button(
                                content="Button",
                                disabled=True,
                                expand=1,
                            ),
                        ]
                    ),
                    ft.Row(
                        [
                            ft.FilledButton(
                                content="Filled",
                                expand=1,
                            ),
                            ft.FilledButton(
                                content="Filled",
                                disabled=True,
                                expand=1,
                            ),
                        ]
                    ),
                    ft.Row(
                        [
                            ft.FilledTonalButton(
                                content="FilledTonal",
                                expand=1,
                            ),
                            ft.FilledTonalButton(
                                content="FilledTonal",
                                disabled=True,
                                expand=1,
                            ),
                        ]
                    ),
                    ft.Row(
                        [
                            ft.OutlinedButton(
                                content="Outlined",
                                expand=1,
                            ),
                            ft.OutlinedButton(
                                content="Outlined",
                                disabled=True,
                                expand=1,
                            ),
                        ]
                    ),
                    ft.Row(
                        [
                            ft.TextButton(
                                content="Text Button",
                                expand=1,
                            ),
                            ft.TextButton(
                                content="Text Button",
                                disabled=True,
                                expand=1,
                            ),
                        ]
                    ),
                ],
            ),
        ],
    )


if __name__ == "__main__":
    ft.run(lambda page: page.render(App))

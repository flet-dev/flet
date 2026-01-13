import flet as ft

FRUITS = [
    "Apple",
    "Mango",
    "Banana",
    "Orange",
    "Pineapple",
    "Strawberry",
]


@ft.component
def GroupTitle(title: str):
    """Small component that renders a title row for a group."""
    return ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Text(
                title,
                style=ft.TextStyle(
                    weight=ft.FontWeight.BOLD,
                    size=16,
                    color=ft.CupertinoColors.LABEL,
                ),
            )
        ],
    )


@ft.component
def App():
    cupertino_picker = ft.CupertinoPicker(
        selected_index=3,
        magnification=1.22,
        squeeze=1.2,
        use_magnifier=True,
        controls=[ft.Text(value=f) for f in FRUITS],
    )

    return ft.Column(
        expand=True,
        alignment=ft.MainAxisAlignment.START,
        controls=[
            GroupTitle("Input Controls"),
            ft.CupertinoCheckbox(label="Checkbox"),
            ft.CupertinoSwitch(label="Switch"),
            ft.CupertinoSlider(min=0, max=100, divisions=10, value=50),
            ft.RadioGroup(
                content=ft.Column(
                    controls=[
                        ft.CupertinoRadio(label="Radio 1", value="r1"),
                        ft.CupertinoRadio(label="Radio 2", value="r2"),
                    ]
                )
            ),
            ft.CupertinoTextField(label="Text Field"),
            GroupTitle("Dialogs"),
            ft.Row(
                controls=[
                    ft.CupertinoButton(
                        "Show Dialog",
                        on_click=lambda e: e.page.show_dialog(
                            ft.CupertinoAlertDialog(
                                title=ft.Text("Hello from Flet!"),
                                actions=[
                                    ft.CupertinoDialogAction(
                                        "OK",
                                        on_click=lambda ev: ev.page.pop_dialog(),
                                    )
                                ],
                            )
                        ),
                    ),
                    ft.CupertinoButton(
                        "Show Picker",
                        on_click=lambda e: e.page.show_dialog(
                            ft.CupertinoBottomSheet(
                                content=cupertino_picker,
                                height=216,
                                padding=ft.Padding.only(top=6),
                            )
                            # ),
                        ),
                    ),
                ]
            ),
            ft.Row(
                controls=[
                    ft.CupertinoButton(
                        "Show DatePicker",
                        on_click=lambda e: e.page.show_dialog(
                            ft.CupertinoBottomSheet(
                                content=ft.CupertinoDatePicker(),
                                height=216,
                                padding=ft.Padding.only(top=6),
                            )
                        ),
                    ),
                    ft.CupertinoButton(
                        "Show TimerPicker",
                        on_click=lambda e: e.page.show_dialog(
                            ft.CupertinoBottomSheet(
                                content=ft.CupertinoTimerPicker(),
                                height=216,
                                padding=ft.Padding.only(top=6),
                            )
                        ),
                    ),
                ]
            ),
            GroupTitle("Buttons"),
            ft.Row(
                controls=[
                    ft.CupertinoButton("CupertinoButton", expand=1),
                    ft.CupertinoButton(
                        content="CupertinoButton",
                        disabled=True,
                        expand=1,
                    ),
                ]
            ),
            ft.Row(
                controls=[
                    ft.CupertinoFilledButton("Filled", expand=1),
                    ft.CupertinoFilledButton(
                        content="Filled",
                        disabled=True,
                        expand=1,
                    ),
                ]
            ),
            ft.Row(
                controls=[
                    ft.CupertinoTintedButton("Tinted", expand=1),
                    ft.CupertinoTintedButton(
                        content="Tinted",
                        disabled=True,
                        expand=1,
                    ),
                ]
            ),
        ],
    )


if __name__ == "__main__":
    ft.run(lambda page: page.render(App))

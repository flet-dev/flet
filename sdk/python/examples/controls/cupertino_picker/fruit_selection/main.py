import flet as ft

FRUITS = [
    "Apple",
    "Mango",
    "Banana",
    "Orange",
    "Pineapple",
    "Strawberry",
]


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    selected_fruit_text = ft.Text(value=FRUITS[3], size=23)

    def handle_selection_change(e: ft.Event[ft.CupertinoPicker]):
        selected_fruit_text.value = FRUITS[int(e.data)]

    cupertino_picker = ft.CupertinoPicker(
        selected_index=3,
        magnification=1.22,
        squeeze=1.2,
        use_magnifier=True,
        on_change=handle_selection_change,
        controls=[ft.Text(value=f) for f in FRUITS],
    )

    page.add(
        ft.SafeArea(
            content=ft.Row(
                tight=True,
                controls=[
                    ft.Text("Selected Fruit:", size=23),
                    ft.TextButton(
                        style=ft.ButtonStyle(color=ft.Colors.BLUE),
                        on_click=lambda _: page.show_dialog(
                            ft.CupertinoBottomSheet(
                                height=216,
                                padding=ft.Padding.only(top=6),
                                content=cupertino_picker,
                            )
                        ),
                        content=selected_fruit_text,
                    ),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)

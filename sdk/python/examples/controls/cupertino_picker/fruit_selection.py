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

    selected_fruit_ref = ft.Ref[ft.Text]()

    def handle_selection_change(e: ft.Event[ft.CupertinoPicker]):
        selected_fruit_ref.current.value = FRUITS[int(e.data)]
        page.update()

    cupertino_picker = ft.CupertinoPicker(
        selected_index=3,
        magnification=1.22,
        squeeze=1.2,
        use_magnifier=True,
        on_change=handle_selection_change,
        controls=[ft.Text(value=f) for f in FRUITS],
    )

    page.add(
        ft.Row(
            tight=True,
            controls=[
                ft.Text("Selected Fruit:", size=23),
                ft.TextButton(
                    content=ft.Text(value=FRUITS[3], ref=selected_fruit_ref, size=23),
                    style=ft.ButtonStyle(color=ft.Colors.BLUE),
                    on_click=lambda e: page.show_dialog(
                        ft.CupertinoBottomSheet(
                            content=cupertino_picker,
                            height=216,
                            padding=ft.Padding.only(top=6),
                        )
                    ),
                ),
            ],
        ),
    )


if __name__ == "__main__":
    ft.run(main)

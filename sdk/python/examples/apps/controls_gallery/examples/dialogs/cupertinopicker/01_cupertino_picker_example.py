import flet as ft

name = "CupertinoPicker example"


def example():
    selected_fruit_ref = ft.Ref[ft.Text]()

    fruits = [
        "Apple",
        "Mango",
        "Banana",
        "Orange",
        "Pineapple",
        "Strawberry",
    ]

    def handle_picker_change(e):
        selected_fruit_ref.current.value = fruits[int(e.data)]
        # e.control.page.update()

    picker = ft.CupertinoPicker(
        selected_index=3,
        # item_extent=40,
        magnification=1.22,
        # diameter_ratio=2,
        squeeze=1.2,
        use_magnifier=True,
        # looping=False,
        on_change=handle_picker_change,
        controls=[ft.Text(f) for f in fruits],
    )

    return ft.Row(
        tight=True,
        controls=[
            ft.Text("Selected Fruit:", size=23),
            ft.TextButton(
                content=ft.Text(fruits[3], size=23, ref=selected_fruit_ref),
                style=ft.ButtonStyle(color=ft.Colors.BLUE),
                on_click=lambda e: e.control.page.open(
                    ft.CupertinoBottomSheet(
                        picker,
                        height=216,
                        bgcolor=ft.CupertinoColors.SYSTEM_BACKGROUND,
                        padding=ft.Padding.only(top=6),
                    )
                ),
            ),
        ],
    )

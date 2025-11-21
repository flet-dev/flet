import flet as ft


def main(page: ft.Page):
    page.title = "BottomSheet Example"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def handle_sheet_dismissal(e: ft.Event[ft.DialogControl]):
        page.add(ft.Text("Bottom sheet dismissed"))

    sheet = ft.BottomSheet(
        on_dismiss=handle_sheet_dismissal,
        content=ft.Container(
            padding=50,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                tight=True,
                controls=[
                    ft.Text("Here is a bottom sheet!"),
                    ft.Button("Dismiss", on_click=lambda _: page.pop_dialog()),
                ],
            ),
        ),
    )

    page.add(
        ft.Button(
            content="Display bottom sheet",
            on_click=lambda e: page.show_dialog(sheet),
        )
    )


if __name__ == "__main__":
    ft.run(main)

import flet as ft


def main(page: ft.Page):
    def open_simple_action(e: ft.Event[ft.Button]):
        page.show_dialog(
            ft.SnackBar(
                ft.Text("The file has been deleted."),
                action="Undo",
                on_action=lambda e: print("Simple Undo clicked"),
            )
        )

    def open_custom_action(e: ft.Event[ft.Button]):
        page.show_dialog(
            ft.SnackBar(
                ft.Text("The directory has been deleted."),
                action=ft.SnackBarAction(
                    label="Undo delete",
                    text_color=ft.Colors.YELLOW,
                    bgcolor=ft.Colors.BLUE,
                    on_click=lambda e: print("Custom Undo clicked"),
                ),
            )
        )

    page.add(
        ft.Button("Open SnackBar with a Simple action", on_click=open_simple_action),
        ft.Button("Open SnackBar with a Custom action", on_click=open_custom_action),
    )


if __name__ == "__main__":
    ft.run(main)

import flet as ft


def main(page: ft.Page):
    page.title = "AlertDialog examples"

    dialog = ft.AlertDialog(
        title=ft.Text("Hello"),
        content=ft.Text("You are notified!"),
        alignment=ft.Alignment.CENTER,
        on_dismiss=lambda e: print("Dialog dismissed!"),
        title_padding=ft.Padding.all(25),
    )

    modal_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Please confirm"),
        content=ft.Text("Do you really want to delete all those files?"),
        actions=[
            ft.TextButton("Yes", on_click=lambda e: page.pop_dialog()),
            ft.TextButton("No", on_click=lambda e: page.pop_dialog()),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )

    page.add(
        ft.Button(
            content="Open dialog",
            on_click=lambda e: page.show_dialog(dialog),
        ),
        ft.Button(
            content="Open modal dialog",
            on_click=lambda e: page.show_dialog(modal_dialog),
        ),
    )


if __name__ == "__main__":
    ft.run(main)

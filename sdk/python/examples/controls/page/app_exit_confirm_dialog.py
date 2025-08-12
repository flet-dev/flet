import flet as ft


def main(page: ft.Page):
    def window_event(e: ft.WindowEvent):
        if e.type == ft.WindowEventType.CLOSE:
            page.show_dialog(confirm_dialog)
            page.update()

    page.window.prevent_close = True
    page.window.on_event = window_event

    async def handle_yes_click(e: ft.Event[ft.ElevatedButton]):
        await page.window.destroy()

    def handle_no_click(e: ft.Event[ft.OutlinedButton]):
        page.pop_dialog()
        page.update()

    confirm_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Please confirm"),
        content=ft.Text("Do you really want to exit this app?"),
        actions=[
            ft.ElevatedButton(content="Yes", on_click=handle_yes_click),
            ft.OutlinedButton(content="No", on_click=handle_no_click),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.add(ft.Text('Try exiting this app by clicking window\'s "Close" button!'))


ft.run(main)

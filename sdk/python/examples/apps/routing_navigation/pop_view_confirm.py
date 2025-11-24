import flet as ft


def main(page: ft.Page):
    page.title = "Routes Example"

    def route_change():
        page.views.clear()
        page.views.append(MainView("/"))
        if page.route == "/store":
            page.views.append(PermissionView("/store"))
        page.update()

    async def view_pop(e: ft.ViewPopEvent):
        if e.view is not None:
            print("View pop:", e.view)
            page.views.remove(e.view)
            top_view = page.views[-1]
            await page.push_route(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    route_change()


class MainView(ft.View):
    def __init__(self, path):
        super().__init__(
            route=path,
            appbar=ft.AppBar(title=ft.Text("Flet app")),
            controls=[
                ft.Button("Go to store", on_click=self.open_store),
            ],
        )

    async def open_store(self, e):
        await self.page.push_route("/store")


class PermissionView(ft.View):
    def __init__(self, path):
        super().__init__(
            route=path,
            appbar=ft.AppBar(title=ft.Text(f"{path} View")),
            can_pop=False,
            on_confirm_pop=self.ask_pop_permission,
        )

    async def ask_pop_permission(self, e):
        async def on_dlg_yes(e):
            self.page.pop_dialog()
            await self.confirm_pop(True)

        async def on_dlg_no(e):
            self.page.pop_dialog()
            await self.confirm_pop(False)

        dlg_modal = ft.AlertDialog(
            title=ft.Text("Please confirm"),
            content=ft.Text("Go home?"),
            actions=[
                ft.TextButton(
                    "Yes",
                    on_click=on_dlg_yes,
                ),
                ft.TextButton(
                    "No",
                    on_click=on_dlg_no,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

        self.page.show_dialog(dlg_modal)
        # await self.confirm_pop(True)


ft.run(main)

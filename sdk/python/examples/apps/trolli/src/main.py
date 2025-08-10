import flet as ft
from app_layout import AppLayout
from board import Board
from data_store import DataStore
from memory_store import InMemoryStore
from user import User


class TrelloApp(AppLayout):
    def __init__(self, page: ft.Page, store: DataStore):
        self.page: ft.Page = page
        self.store: DataStore = store
        self.user: str | None = None
        self.page.on_route_change = self.route_change
        self.boards = self.store.get_boards()
        self.login_profile_button = ft.PopupMenuItem(text="Log in", on_click=self.login)
        self.appbar_items = [
            self.login_profile_button,
            ft.PopupMenuItem(),  # divider
            ft.PopupMenuItem(text="Settings"),
        ]
        self.appbar = ft.AppBar(
            leading=ft.Icon(ft.Icons.GRID_GOLDENRATIO_ROUNDED),
            leading_width=100,
            title=ft.Text(
                "Trolli",
                font_family="Pacifico",
                size=32,
                text_align=ft.TextAlign.START,
            ),
            center_title=False,
            toolbar_height=75,
            bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_700,
            actions=[
                ft.Container(
                    content=ft.PopupMenuButton(items=self.appbar_items),
                    margin=ft.margin.only(left=50, right=25),
                )
            ],
        )
        self.page.appbar = self.appbar

        self.page.update()
        super().__init__(
            self,
            self.page,
            self.store,
            tight=True,
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

    def initialize(self):
        self.page.views.append(
            ft.View(
                "/",
                [self.appbar, self],
                padding=ft.Padding.all(0),
                bgcolor=ft.Colors.BLUE_GREY_200,
            )
        )
        self.page.update()
        # create an initial board for demonstration if no boards
        if len(self.boards) == 0:
            self.create_new_board("My First Board")
        self.page.go("/")

    async def login(self, e):
        async def close_dlg(e):
            if user_name.value == "" or password.value == "":
                user_name.error_text = "Please provide username"
                password.error_text = "Please provide password"
                self.page.update()
                return
            else:
                user = User(user_name.value, password.value)
                if user not in self.store.get_users():
                    self.store.add_user(user)
                self.user = user_name.value
                await self.page.shared_preferences.set_async(
                    "current_user", user_name.value
                )

            self.page.close(dialog)
            current_user = await self.page.shared_preferences.get_async("current_user")
            self.appbar_items[0] = ft.PopupMenuItem(content=f"{current_user}'s Profile")
            self.page.update()

        user_name = ft.TextField(label="User name")
        password = ft.TextField(label="Password", password=True)
        dialog = ft.AlertDialog(
            title=ft.Text("Please enter your login credentials"),
            content=ft.Column(
                [
                    user_name,
                    password,
                    ft.ElevatedButton(text="Login", on_click=close_dlg),
                ],
                tight=True,
            ),
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        self.page.open(dialog)

    def route_change(self, e):
        troute = ft.TemplateRoute(self.page.route)
        if troute.match("/"):
            self.page.go("/boards")
        elif troute.match("/board/:id"):
            if int(troute.id) > len(self.store.get_boards()):
                self.page.go("/")
                return
            self.set_board_view(int(troute.id))
        elif troute.match("/boards"):
            self.set_all_boards_view()
        elif troute.match("/members"):
            self.set_members_view()
        self.page.update()

    async def add_board(self, e):
        def close_dlg(e):
            if (hasattr(e.control, "text") and e.control.text != "Cancel") or (
                type(e.control) is ft.TextField and e.control.value != ""
            ):
                self.create_new_board(dialog_text.value)
            self.page.close(dialog)
            self.page.update()

        def textfield_change(e):
            if dialog_text.value == "":
                create_button.disabled = True
            else:
                create_button.disabled = False
            self.page.update()

        dialog_text = ft.TextField(
            label="New Board Name", on_submit=close_dlg, on_change=textfield_change
        )
        create_button = ft.ElevatedButton(
            text="Create", bgcolor=ft.Colors.BLUE_200, on_click=close_dlg, disabled=True
        )
        dialog = ft.AlertDialog(
            title=ft.Text("Name your new board"),
            content=ft.Column(
                [
                    dialog_text,
                    ft.Row(
                        [
                            ft.ElevatedButton(text="Cancel", on_click=close_dlg),
                            create_button,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
                tight=True,
            ),
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        self.page.open(dialog)
        dialog.open = True
        self.page.update()
        await dialog_text.focus_async()

    def create_new_board(self, board_name):
        new_board = Board(self, self.store, board_name, self.page)
        self.store.add_board(new_board)
        self.hydrate_all_boards_view()

    def delete_board(self, e):
        self.store.remove_board(e.control.data)
        self.set_all_boards_view()


def main(page: ft.Page):
    page.title = "Flet Trello clone"
    page.padding = 0
    page.theme = ft.Theme(font_family="Verdana")
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme.page_transitions.windows = "cupertino"
    page.fonts = {"Pacifico": "Pacifico-Regular.ttf"}
    page.bgcolor = ft.Colors.BLUE_GREY_200
    app = TrelloApp(page, InMemoryStore())
    page.add(app)
    page.update()
    app.initialize()


print("flet version: ", ft.version.version)
print("flet path: ", ft.__file__)
ft.run(target=main, assets_dir="../assets")

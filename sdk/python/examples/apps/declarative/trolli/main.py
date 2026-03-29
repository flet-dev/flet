import asyncio
import logging
from typing import Optional

from components import BoardsView, BoardView, Sidebar, TrolliAppBar
from models import TrolliState

import flet as ft

logging.basicConfig(level=logging.INFO)
logging.getLogger("flet_components").setLevel(logging.INFO)


def _init_demo_data(app: TrolliState) -> None:
    if app.boards:
        return
    board = app.create_board("My First Board")
    board.add_list("To Do", ft.Colors.AMBER_200)
    board.add_list("Doing", ft.Colors.LIGHT_BLUE_200)
    board.add_list("Done", ft.Colors.LIGHT_GREEN_200)
    board.lists[0].add_card("Drag cards between lists")
    board.lists[0].add_card("Drag lists to reorder")
    board.lists[1].add_card("Add a list from the button")


@ft.component
def App():
    app, _ = ft.use_state(lambda: TrolliState(route=ft.context.page.route))
    ft.context.page.padding = 0
    ft.context.page.theme_mode = ft.ThemeMode.LIGHT
    ft.context.page.fonts = {"Pacifico": "Pacifico-Regular.ttf"}
    ft.context.page.bgcolor = ft.Colors.BLUE_GREY_200
    if ft.context.page.route == "/":
        asyncio.create_task(ft.context.page.push_route("/boards"))
        # ft.context.page.go("/boards")

    def parse_board_id_from_route(route: str) -> Optional[int]:
        troute = ft.TemplateRoute(route)
        if not troute.match("/board/:id"):
            return None

        raw = getattr(troute, "id", None)
        if not isinstance(raw, str):
            return None
        try:
            return int(raw)
        except ValueError:
            return None

    def route_change(e: ft.RouteChangeEvent):
        # Keep route as the single source of truth for navigation-related UI.
        app.route = e.route

        if e.route.startswith("/board/"):
            board_id = parse_board_id_from_route(e.route)
            if board_id is None or app.get_board_by_id(board_id) is None:
                asyncio.create_task(ft.context.page.push_route("/boards"))
                app.active_screen = "boards"
                app.current_board_id = None
                app.route = "/boards"
                return

        if e.route in ("/", "/boards"):
            app.active_screen = "boards"
            app.current_board_id = None
        elif e.route == "/members":
            app.active_screen = "members"
            app.current_board_id = None
        elif e.route == "/settings":
            app.active_screen = "settings"
            app.current_board_id = None
        elif e.route.startswith("/board/"):
            app.active_screen = "board"
            app.current_board_id = board_id
        else:
            asyncio.create_task(ft.context.page.push_route("/boards"))
            app.active_screen = "boards"
            app.current_board_id = None
            app.route = "/boards"
            return

    ft.context.page.on_route_change = route_change

    def redirect_unknown_board():
        if not app.route.startswith("/board/"):
            return
        board_id = parse_board_id_from_route(app.route)
        if board_id is None or app.get_board_by_id(board_id) is None:
            asyncio.create_task(ft.context.page.push_route("/boards"))

    # ft.on_updated(redirect_unknown_board, [app.route])

    ft.on_mounted(lambda: _init_demo_data(app))

    def toggle_sidebar(_: ft.Event[ft.IconButton]):
        app.nav_visible = not app.nav_visible

    board_id = parse_board_id_from_route(app.route)
    board = app.get_board_by_id(board_id) if board_id is not None else None

    if app.active_screen == "boards":
        content: ft.Control = BoardsView(app)
    elif app.active_screen == "members":
        content = ft.Text("Members view placeholder", align=ft.Alignment.CENTER)
    elif app.active_screen == "settings":
        content = ft.Text("Settings view placeholder", align=ft.Alignment.CENTER)
    else:
        board = (
            app.get_board_by_id(app.current_board_id) if app.current_board_id else None
        )
        content = BoardView(board) if board else BoardsView(app)

    return ft.SafeArea(
        expand=True,
        content=ft.Column(
            expand=True,
            spacing=0,
            controls=[
                TrolliAppBar(app),
                ft.Row(
                    expand=True,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        Sidebar(app),
                        ft.Stack(
                            fit=ft.StackFit.LOOSE,
                            expand=True,
                            controls=[
                                ft.Container(
                                    padding=ft.Padding.only(left=10, right=10, top=10),
                                    content=content,
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_CIRCLE_LEFT,
                                    selected=not app.nav_visible,
                                    selected_icon=ft.Icons.ARROW_CIRCLE_RIGHT,
                                    icon_color=ft.Colors.BLUE_GREY_400,
                                    icon_size=20,
                                    padding=0,
                                    on_click=toggle_sidebar,
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    )


def main(page: ft.Page):
    page.render(App)


if __name__ == "__main__":
    ft.run(main, route_url_strategy="hash")

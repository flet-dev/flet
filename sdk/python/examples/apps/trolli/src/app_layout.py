import flet as ft
from board import Board
from data_store import DataStore
from sidebar import Sidebar


class AppLayout(ft.Row):
    def __init__(self, app, page: ft.Page, store: DataStore, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.page: ft.Page = page
        self.page.on_resized = self.page_resize
        self.store: DataStore = store
        self.toggle_nav_rail_button = ft.IconButton(
            icon=ft.Icons.ARROW_CIRCLE_LEFT,
            icon_color=ft.Colors.BLUE_GREY_400,
            selected=False,
            selected_icon=ft.Icons.ARROW_CIRCLE_RIGHT,
            on_click=self.toggle_nav_rail,
        )
        self.sidebar = Sidebar(self, self.store)
        self.members_view = ft.Text("members view")
        self.all_boards_view = ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(
                            ft.Text(
                                value="Your Boards",
                                theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                            ),
                            expand=True,
                            padding=ft.Padding.only(top=15),
                        ),
                        ft.Container(
                            ft.TextButton(
                                "Add new board",
                                icon=ft.Icons.ADD,
                                on_click=self.app.add_board,
                                style=ft.ButtonStyle(
                                    bgcolor={
                                        ft.ControlState.DEFAULT: ft.Colors.BLUE_200,
                                        ft.ControlState.HOVERED: ft.Colors.BLUE_400,
                                    },
                                    shape={
                                        ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(
                                            radius=3
                                        )
                                    },
                                ),
                            ),
                            padding=ft.Padding.only(right=50, top=15),
                        ),
                    ]
                ),
                ft.Row(
                    [
                        ft.TextField(
                            hint_text="Search all boards",
                            autofocus=False,
                            content_padding=ft.Padding.only(left=10),
                            width=200,
                            height=40,
                            text_size=12,
                            border_color=ft.Colors.BLACK26,
                            focused_border_color=ft.Colors.BLUE_ACCENT,
                            suffix_icon=ft.Icons.SEARCH,
                        )
                    ]
                ),
                ft.Row([ft.Text("No Boards to Display")]),
            ],
            expand=True,
        )
        self._active_view: ft.Control = self.all_boards_view

        self.controls = [self.sidebar, self.toggle_nav_rail_button, self.active_view]

    @property
    def active_view(self):
        return self._active_view

    @active_view.setter
    def active_view(self, view):
        self._active_view = view
        self.controls[-1] = self._active_view
        self.sidebar.sync_board_destinations()
        self.page.update()

    def set_board_view(self, i):
        self.active_view = self.store.get_boards()[i]
        self.sidebar.bottom_nav_rail.selected_index = i
        self.sidebar.top_nav_rail.selected_index = None
        self.page_resize()
        self.page.update()

    def set_all_boards_view(self):
        self.active_view = self.all_boards_view
        self.hydrate_all_boards_view()
        self.sidebar.top_nav_rail.selected_index = 0
        self.sidebar.bottom_nav_rail.selected_index = None
        self.page.update()

    def set_members_view(self):
        self.active_view = self.members_view
        self.sidebar.top_nav_rail.selected_index = 1
        self.sidebar.bottom_nav_rail.selected_index = None
        self.page.update()

    def page_resize(self, e=None):
        if type(self.active_view) is Board:
            self.active_view.resize(
                self.sidebar.visible, self.page.width, self.page.height
            )
        self.page.update()

    def hydrate_all_boards_view(self):
        self.all_boards_view.controls[-1] = ft.Row(
            [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(
                                content=ft.Text(value=b.name),
                                data=b,
                                expand=True,
                                on_click=self.board_click,
                            ),
                            ft.Container(
                                content=ft.PopupMenuButton(
                                    items=[
                                        ft.PopupMenuItem(
                                            content=ft.Text(
                                                value="Delete",
                                                theme_style=ft.TextThemeStyle.LABEL_MEDIUM,
                                                text_align=ft.TextAlign.CENTER,
                                            ),
                                            on_click=self.app.delete_board,
                                            data=b,
                                        ),
                                        ft.PopupMenuItem(),
                                        ft.PopupMenuItem(
                                            content=ft.Text(
                                                value="Archive",
                                                theme_style=ft.TextThemeStyle.LABEL_MEDIUM,
                                                text_align=ft.TextAlign.CENTER,
                                            ),
                                        ),
                                    ]
                                ),
                                padding=ft.Padding.only(right=-10),
                                border_radius=ft.border_radius.all(3),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    border=ft.border.all(1, ft.Colors.BLACK38),
                    border_radius=ft.border_radius.all(5),
                    bgcolor=ft.Colors.WHITE60,
                    padding=ft.Padding.all(10),
                    width=250,
                    data=b,
                )
                for b in self.store.get_boards()
            ],
            wrap=True,
        )
        self.sidebar.sync_board_destinations()

    def board_click(self, e):
        self.sidebar.bottom_nav_change(self.store.get_boards().index(e.control.data))

    def toggle_nav_rail(self, e):
        self.sidebar.visible = not self.sidebar.visible
        self.toggle_nav_rail_button.selected = not self.toggle_nav_rail_button.selected
        self.page_resize()
        self.page.update()

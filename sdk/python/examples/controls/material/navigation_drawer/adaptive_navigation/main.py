import flet as ft

DESTINATIONS = [
    ("Messages", ft.Icons.WIDGETS_OUTLINED, ft.Icons.WIDGETS),
    ("Profile", ft.Icons.FORMAT_PAINT_OUTLINED, ft.Icons.FORMAT_PAINT),
    ("Settings", ft.Icons.SETTINGS_OUTLINED, ft.Icons.SETTINGS),
]


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0

    screen_index = 0

    def build_page_index_text() -> ft.Text:
        return ft.Text(f"Page Index = {screen_index}", size=24)

    def set_screen(index: int):
        nonlocal screen_index
        screen_index = index
        render()

    def build_navigation_bar() -> ft.NavigationBar:
        def handle_nav_bar_change(e: ft.Event[ft.NavigationBar]):
            set_screen(e.control.selected_index)

        return ft.NavigationBar(
            selected_index=screen_index,
            on_change=handle_nav_bar_change,
            destinations=[
                ft.NavigationBarDestination(
                    label=label,
                    icon=icon,
                    selected_icon=selected_icon,
                )
                for label, icon, selected_icon in DESTINATIONS
            ],
        )

    def build_navigation_rail() -> ft.NavigationRail:
        def handle_nav_rail_change(e: ft.Event[ft.NavigationRail]):
            if e.control.selected_index is not None:
                set_screen(e.control.selected_index)

        return ft.NavigationRail(
            min_width=50,
            selected_index=screen_index,
            use_indicator=True,
            on_change=handle_nav_rail_change,
            destinations=[
                ft.NavigationRailDestination(
                    label=label,
                    icon=icon,
                    selected_icon=selected_icon,
                )
                for label, icon, selected_icon in DESTINATIONS
            ],
        )

    def build_end_drawer() -> ft.NavigationDrawer:
        async def handle_drawer_change(e: ft.Event[ft.NavigationDrawer]):
            set_screen(e.control.selected_index)
            await page.close_end_drawer()

        return ft.NavigationDrawer(
            selected_index=screen_index,
            on_change=handle_drawer_change,
            controls=[
                ft.Container(
                    padding=ft.Padding.only(left=28, top=16, right=16, bottom=10),
                    content=ft.Text(
                        "Header", theme_style=ft.TextThemeStyle.TITLE_SMALL
                    ),
                ),
                *[
                    ft.NavigationDrawerDestination(
                        label=label,
                        icon=icon,
                        selected_icon=selected_icon,
                    )
                    for label, icon, selected_icon in DESTINATIONS
                ],
            ],
        )

    def build_bottom_bar_layout() -> ft.SafeArea:
        return ft.SafeArea(
            expand=True,
            content=ft.Container(
                expand=True,
                alignment=ft.Alignment.CENTER,
                content=build_page_index_text(),
            ),
        )

    def build_drawer_layout() -> ft.SafeArea:
        async def open_drawer(e: ft.Event[ft.Button]):
            await page.show_end_drawer()

        return ft.SafeArea(
            expand=True,
            avoid_intrusions_top=False,
            avoid_intrusions_bottom=False,
            content=ft.Row(
                expand=True,
                controls=[
                    ft.Container(
                        padding=ft.Padding.symmetric(horizontal=5),
                        content=build_navigation_rail(),
                    ),
                    ft.VerticalDivider(thickness=1, width=1),
                    ft.Column(
                        expand=True,
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            build_page_index_text(),
                            ft.Button("Open Drawer", on_click=open_drawer),
                        ],
                    ),
                ],
            ),
        )

    def render():
        page.clean()
        if (page.width or page.window.width) >= 450:  # wide layout
            page.navigation_bar = None
            page.end_drawer = build_end_drawer()
            page.add(build_drawer_layout())
        else:  # narrow layout
            page.end_drawer = None
            page.navigation_bar = build_navigation_bar()
            page.add(build_bottom_bar_layout())
        page.update()

    page.on_resize = lambda e: render()
    render()


if __name__ == "__main__":
    ft.run(main)

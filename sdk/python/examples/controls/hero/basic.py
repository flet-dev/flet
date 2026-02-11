import flet as ft


def main(page: ft.Page):
    hero_tag = "demo-hero-card"

    def build_card(size: int, label: str) -> ft.Container:
        icon_size = max(24, int(size * 0.28))
        return ft.Container(
            width=size,
            height=size,
            border_radius=ft.BorderRadius.all(20),
            gradient=ft.LinearGradient(
                begin=ft.Alignment.TOP_LEFT,
                end=ft.Alignment.BOTTOM_RIGHT,
                colors=[ft.Colors.BLUE_700, ft.Colors.CYAN_400],
            ),
            alignment=ft.Alignment.CENTER,
            content=ft.Stack(
                fit=ft.StackFit.EXPAND,
                controls=[
                    ft.Container(
                        alignment=ft.Alignment.CENTER,
                        content=ft.Icon(
                            ft.Icons.ROCKET_LAUNCH,
                            size=icon_size,
                            color=ft.Colors.WHITE,
                        ),
                    ),
                    ft.Container(
                        alignment=ft.Alignment.BOTTOM_CENTER,
                        padding=ft.Padding.only(left=8, right=8, bottom=10),
                        content=ft.Text(
                            label,
                            color=ft.Colors.WHITE,
                            weight=ft.FontWeight.BOLD,
                            size=12,
                            no_wrap=True,
                            max_lines=1,
                            overflow=ft.TextOverflow.ELLIPSIS,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ),
                ],
            ),
        )

    async def go_to_details(_):
        await page.push_route("/details")

    async def go_home(_):
        await page.push_route("/")

    def build_home_view() -> ft.View:
        return ft.View(
            route="/",
            appbar=ft.AppBar(title=ft.Text("Hero animation")),
            controls=[
                ft.Container(
                    expand=True,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                        controls=[
                            ft.Text("Tap the card to navigate"),
                            ft.GestureDetector(
                                mouse_cursor=ft.MouseCursor.CLICK,
                                on_tap=go_to_details,
                                content=ft.Hero(
                                    tag=hero_tag,
                                    content=build_card(130, "Open details"),
                                ),
                            ),
                        ],
                    ),
                )
            ],
        )

    def build_details_view() -> ft.View:
        return ft.View(
            route="/details",
            appbar=ft.AppBar(title=ft.Text("Details")),
            controls=[
                ft.Container(
                    expand=True,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                        controls=[
                            ft.Hero(
                                tag=hero_tag,
                                transition_on_user_gestures=True,
                                content=build_card(280, "Details"),
                            ),
                            ft.Button("Back", on_click=go_home),
                        ],
                    ),
                )
            ],
        )

    def route_change(e: ft.RouteChangeEvent = None):
        page.views.clear()
        page.views.append(build_home_view())
        if page.route == "/details":
            page.views.append(build_details_view())
        page.update()

    async def view_pop(e: ft.ViewPopEvent):
        if e.view is not None:
            page.views.remove(e.view)
            await page.push_route(page.views[-1].route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    route_change()


if __name__ == "__main__":
    ft.run(main)

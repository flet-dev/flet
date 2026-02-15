import flet as ft

PRODUCTS = [
    {
        "id": 1,
        "name": "Comet",
        "subtitle": "Fast launch profile",
        "description": "Balanced setup for quick iteration and lightweight payloads.",
        "icon": ft.Icons.ROCKET_LAUNCH,
        "start_color": ft.Colors.BLUE_700,
        "end_color": ft.Colors.CYAN_400,
    },
    {
        "id": 2,
        "name": "Nebula",
        "subtitle": "Visual pipeline",
        "description": "Optimized for rich UI transitions and animated data surfaces.",
        "icon": ft.Icons.AUTO_AWESOME,
        "start_color": ft.Colors.DEEP_PURPLE_700,
        "end_color": ft.Colors.PINK_400,
    },
    {
        "id": 3,
        "name": "Orbit",
        "subtitle": "Reliable baseline",
        "description": "Stable profile focused on consistency and performance.",
        "icon": ft.Icons.PUBLIC,
        "start_color": ft.Colors.GREEN_700,
        "end_color": ft.Colors.LIGHT_GREEN_400,
    },
    {
        "id": 4,
        "name": "Aurora",
        "subtitle": "Analytics focus",
        "description": "Configured for telemetry-heavy apps and live metrics.",
        "icon": ft.Icons.ANALYTICS,
        "start_color": ft.Colors.ORANGE_700,
        "end_color": ft.Colors.AMBER_400,
    },
    {
        "id": 5,
        "name": "Pulse",
        "subtitle": "Real-time profile",
        "description": "Tuned for frequent updates, messaging, and event streams.",
        "icon": ft.Icons.BOLT,
        "start_color": ft.Colors.RED_700,
        "end_color": ft.Colors.DEEP_ORANGE_400,
    },
]


def hero_tag(product_id: int) -> str:
    return f"product-hero-{product_id}"


def main(page: ft.Page):
    def product_by_id(product_id: int):
        for product in PRODUCTS:
            if product["id"] == product_id:
                return product
        return None

    def route_product_id(route: str):
        segments = [segment for segment in route.split("/") if segment]
        if len(segments) != 2 or segments[0] != "product":
            return None
        try:
            return int(segments[1])
        except ValueError:
            return None

    async def open_product(product_id: int):
        await page.push_route(f"/product/{product_id}")

    async def back_to_gallery(e: ft.Event[ft.Button]):
        await page.push_route("/")

    def build_hero_tile(product: dict, size: int) -> ft.Hero:
        icon_size = max(24, int(size * 0.4))
        return ft.Hero(
            tag=hero_tag(product["id"]),
            transition_on_user_gestures=True,
            content=ft.Container(
                width=size,
                height=size,
                border_radius=ft.BorderRadius.all(20),
                gradient=ft.LinearGradient(
                    begin=ft.Alignment.TOP_LEFT,
                    end=ft.Alignment.BOTTOM_RIGHT,
                    colors=[product["start_color"], product["end_color"]],
                ),
                alignment=ft.Alignment.CENTER,
                content=ft.Icon(product["icon"], color=ft.Colors.WHITE, size=icon_size),
            ),
        )

    def build_home_view() -> ft.View:
        rows: list[ft.Control] = []
        for product in PRODUCTS:
            rows.append(
                ft.GestureDetector(
                    mouse_cursor=ft.MouseCursor.CLICK,
                    on_tap=lambda _, pid=product["id"]: page.run_task(
                        open_product, pid
                    ),
                    content=ft.Card(
                        content=ft.Container(
                            padding=12,
                            content=ft.Row(
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=12,
                                controls=[
                                    build_hero_tile(product, 78),
                                    ft.Column(
                                        spacing=4,
                                        controls=[
                                            ft.Text(
                                                product["name"],
                                                size=18,
                                                weight=ft.FontWeight.W_600,
                                            ),
                                            ft.Text(
                                                product["subtitle"],
                                                color=ft.Colors.ON_SURFACE_VARIANT,
                                            ),
                                            ft.Text(
                                                "Tap to view details",
                                                size=12,
                                                color=ft.Colors.PRIMARY,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        )
                    ),
                )
            )

        return ft.View(
            route="/",
            appbar=ft.AppBar(title=ft.Text("Hero gallery")),
            controls=[
                ft.Column(
                    expand=True,
                    spacing=10,
                    scroll=ft.ScrollMode.AUTO,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            "Each card has a unique Hero tag. "
                            "Open any item to see a matched transition.",
                            color=ft.Colors.ON_SURFACE_VARIANT,
                        ),
                        *rows,
                    ],
                )
            ],
        )

    def build_details_view(product: dict) -> ft.View:
        return ft.View(
            route=f"/product/{product['id']}",
            appbar=ft.AppBar(title=ft.Text(product["name"])),
            controls=[
                ft.Column(
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=16,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Container(height=8),
                        build_hero_tile(product, 220),
                        ft.Text(
                            product["subtitle"],
                            size=20,
                            weight=ft.FontWeight.W_600,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Container(
                            width=520,
                            content=ft.Text(
                                product["description"],
                                text_align=ft.TextAlign.CENTER,
                                color=ft.Colors.ON_SURFACE_VARIANT,
                            ),
                        ),
                        ft.Button("Back to gallery", on_click=back_to_gallery),
                    ],
                )
            ],
        )

    def route_change(e: ft.RouteChangeEvent = None):
        page.views.clear()
        page.views.append(build_home_view())

        pid = route_product_id(page.route)
        if pid is not None:
            product = product_by_id(pid)
            if product is not None:
                page.views.append(build_details_view(product))

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

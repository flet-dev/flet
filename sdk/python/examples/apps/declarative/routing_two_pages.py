import asyncio
import logging
from collections.abc import Callable
from dataclasses import dataclass

import flet as ft

logging.basicConfig(level=logging.INFO)
logging.getLogger("flet_components").setLevel(logging.INFO)
# logging.getLogger("flet_object_patch").setLevel(logging.DEBUG)


@dataclass(frozen=True)
class ThemeContextValue:
    mode: ft.ThemeMode
    toggle: Callable[[], None]


ThemeContext = ft.create_context(ThemeContextValue(ft.ThemeMode.LIGHT, lambda: None))


@ft.observable
@dataclass
class AppModel:
    route: str
    theme_mode: ft.ThemeMode = ft.ThemeMode.LIGHT

    def route_change(self, e: ft.RouteChangeEvent):
        print("Route changed from:", self.route, "to:", e.route)
        self.route = e.route

    async def view_popped(self, e: ft.ViewPopEvent):
        print("View popped")
        views = ft.unwrap_component(ft.context.page.views)
        if len(views) > 1:
            await ft.context.page.push_route(views[-2].route)

    def toggle_theme(self):
        self.theme_mode = (
            ft.ThemeMode.DARK
            if self.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )


@ft.component
def ThemeToggle():
    theme = ft.use_context(ThemeContext)
    return ft.Switch(
        label="Dark mode" if theme.mode == ft.ThemeMode.LIGHT else "Light mode",
        value=theme.mode == ft.ThemeMode.DARK,
        on_change=lambda: theme.toggle(),
    )


@ft.component
def AppBar():
    return ft.AppBar(
        title=ft.Text("Flet app"),
        bgcolor=ft.Colors.SURFACE_BRIGHT,
        actions=[ThemeToggle()],
    )


@ft.component
def NavBar():
    tabs = [
        ("Home", "/", ft.Icons.HOME),
        ("Travel", "/travel", ft.Icons.EMOJI_TRANSPORTATION),
        ("Settings", "/settings", ft.Icons.SETTINGS),
    ]

    async def navigate_to(e: ft.Event[ft.NavigationBar]):
        await ft.context.page.push_route(tabs[e.control.selected_index][1])

    return ft.NavigationBar(
        selected_index=next(
            (i for i, t in enumerate(tabs) if t[1] == ft.context.page.route), 0
        ),
        on_change=navigate_to,
        destinations=[ft.NavigationBarDestination(icon=t[2], label=t[0]) for t in tabs],
    )


@ft.component
def RoutingExample():
    app, _ = ft.use_state(AppModel(route=ft.context.page.route))

    # subscribe to page events as soon as possible
    ft.context.page.on_route_change = app.route_change
    ft.context.page.on_view_pop = app.view_popped

    # stable callback (doesn’t change identity each render)
    toggle = ft.use_callback(lambda: app.toggle_theme(), dependencies=[app.theme_mode])

    # memoize the provided value so its identity changes only when mode changes
    theme_value = ft.use_memo(
        lambda: ThemeContextValue(mode=app.theme_mode, toggle=toggle),
        dependencies=[app.theme_mode, toggle],
    )

    ft.on_mounted(
        lambda: print("Page size:", ft.context.page.width, ft.context.page.height)
    )

    def update_theme_mode():
        print("Theme mode changed to:", app.theme_mode)
        ft.context.page.theme_mode = app.theme_mode

    ft.on_updated(update_theme_mode, [app.theme_mode])

    return ThemeContext(
        theme_value,
        lambda: [
            ft.View(
                route="/travel",
                appbar=AppBar(),
                navigation_bar=NavBar(),
                transition=ft.ViewTransition.NONE,
                controls=[
                    ft.Text("Welcome to the Travel page!"),
                ],
            )
            if app.route == "/travel"
            else ft.View(
                route="/settings",
                appbar=AppBar(),
                navigation_bar=NavBar(),
                transition=ft.ViewTransition.NONE,
                controls=[
                    ft.Text("Welcome to the Settings page!"),
                ],
            )
            if app.route == "/settings"
            else ft.View(
                route="/",
                appbar=AppBar(),
                navigation_bar=NavBar(),
                transition=ft.ViewTransition.NONE,
                controls=[
                    ft.Button(
                        "Visit Store",
                        on_click=lambda _: asyncio.create_task(
                            ft.context.page.push_route("/store")
                        ),
                    ),
                    ft.Button(
                        "Do something",
                        on_click=lambda _: asyncio.create_task(
                            ft.context.page.push_route("/do-something")
                        ),
                    ),
                ],
            ),
            *(
                [
                    ft.View(
                        route="/store",
                        appbar=AppBar(),
                        controls=[
                            ft.Button(
                                "Go Home",
                                on_click=lambda _: asyncio.create_task(
                                    ft.context.page.push_route("/")
                                ),
                            ),
                        ],
                    )
                ]
                if app.route == "/store"
                else []
            ),
        ],
    )


ft.run(lambda page: page.render_views(RoutingExample))

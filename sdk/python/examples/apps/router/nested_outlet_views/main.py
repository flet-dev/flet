import flet as ft


@ft.component
def Home():
    return ft.View(
        route="/",
        can_pop=False,
        appbar=ft.AppBar(title=ft.Text("Home")),
        controls=[
            ft.Text("Welcome!", size=24),
            ft.Button(
                "Browse Products",
                on_click=lambda: ft.context.page.navigate("/products"),
            ),
        ],
    )


@ft.component
def ProductsList():
    """Returns a regular control — the layout provides the View."""
    return ft.Column(
        [
            ft.Text("All Products", size=24),
            ft.Button(
                "View Product #1",
                on_click=lambda: ft.context.page.navigate("/products/1"),
            ),
            ft.Button(
                "View Product #2",
                on_click=lambda: ft.context.page.navigate("/products/2"),
            ),
        ]
    )


@ft.component
def ProductDetails():
    """Returns a regular control — the layout provides the View."""
    params = ft.use_route_params()
    return ft.Text(f"Product #{params['pid']}", size=24)


@ft.component
def ProductsLayout():
    """Shared layout — wraps each child route in a View with AppBar + footer."""
    outlet = ft.use_route_outlet()
    return ft.View(
        # use_view_path() returns the per-view resolved URL (unique per level)
        # — required for Flutter Navigator keying when the layout wraps
        # multiple child routes.
        route=ft.use_view_path(),
        appbar=ft.AppBar(
            title=ft.Text("Products"),
            bgcolor=ft.Colors.SURFACE_BRIGHT,
        ),
        controls=[
            ft.Container(content=outlet, padding=20, expand=True),
            ft.Divider(),
            ft.Text("Products Footer", text_align=ft.TextAlign.CENTER),
        ],
    )


@ft.component
def App():
    return ft.Router(
        [
            ft.Route(
                component=Home,
                children=[
                    ft.Route(
                        path="products",
                        component=ProductsLayout,
                        outlet=True,
                        children=[
                            ft.Route(
                                component=ProductsList,
                                children=[
                                    ft.Route(path=":pid", component=ProductDetails),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
        manage_views=True,
    )


if __name__ == "__main__":
    ft.run(lambda page: page.render_views(App))

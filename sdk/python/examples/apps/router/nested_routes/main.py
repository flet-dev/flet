import flet as ft


@ft.component
def Home():
    return ft.View(
        route="/",
        can_pop=False,
        appbar=ft.AppBar(title=ft.Text("Home")),
        controls=[
            ft.Text("Home", size=24),
            ft.Button(
                "Go to Products",
                on_click=lambda: ft.context.page.navigate("/products"),
            ),
        ],
    )


@ft.component
def ProductsList():
    return ft.View(
        route="/products",
        appbar=ft.AppBar(title=ft.Text("Products")),
        controls=[
            ft.Text("All Products", size=24),
            ft.Button(
                "View Product #1",
                on_click=lambda: ft.context.page.navigate("/products/1"),
            ),
            ft.Button(
                "View Product #2",
                on_click=lambda: ft.context.page.navigate("/products/2"),
            ),
        ],
    )


@ft.component
def ProductDetails():
    params = ft.use_route_params()
    return ft.View(
        route=f"/products/{params['pid']}",
        appbar=ft.AppBar(title=ft.Text(f"Product #{params['pid']}")),
        controls=[
            ft.Text(f"Details for product #{params['pid']}", size=24),
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
                        component=ProductsList,
                        children=[
                            ft.Route(path=":pid", component=ProductDetails),
                        ],
                    ),
                ],
            ),
        ],
        manage_views=True,
    )


if __name__ == "__main__":
    ft.run(lambda page: page.render_views(App))

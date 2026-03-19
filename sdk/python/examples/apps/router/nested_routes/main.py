"""Nested routes — parent/child route hierarchy."""

import flet as ft


@ft.component
def Home():
    return ft.Text("Home", size=24)


@ft.component
def ProductsList():
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
    params = ft.use_route_params()
    return ft.Column(
        [
            ft.Text(f"Product #{params['pid']}", size=24),
            ft.Button(
                "Back to Products",
                on_click=lambda: ft.context.page.navigate("/products"),
            ),
        ]
    )


@ft.component
def App():
    return ft.SafeArea(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Button(
                            "Home",
                            on_click=lambda: ft.context.page.navigate("/"),
                        ),
                        ft.Button(
                            "Products",
                            on_click=lambda: ft.context.page.navigate("/products"),
                        ),
                    ]
                ),
                ft.Router(
                    [
                        ft.Route(index=True, component=Home),
                        ft.Route(
                            path="products",
                            children=[
                                ft.Route(index=True, component=ProductsList),
                                ft.Route(path=":pid", component=ProductDetails),
                            ],
                        ),
                    ]
                ),
            ]
        )
    )


if __name__ == "__main__":
    ft.run(lambda page: page.render(App))

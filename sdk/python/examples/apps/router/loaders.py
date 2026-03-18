"""Loaders — data loading with loader and use_route_loader_data()."""

import flet as ft


# Simulated data loaders
def home_loader(params):
    return {"title": "Home", "message": "Welcome to the app!"}


def products_loader(params):
    return {
        "products": [
            {"id": 1, "name": "Widget A", "price": 9.99},
            {"id": 2, "name": "Gadget B", "price": 24.99},
            {"id": 3, "name": "Doohickey C", "price": 4.99},
        ]
    }


def product_detail_loader(params):
    pid = params.get("pid", "?")
    # In a real app, you'd fetch from a database or API
    products = {
        "1": {"id": 1, "name": "Widget A", "price": 9.99, "stock": 42},
        "2": {"id": 2, "name": "Gadget B", "price": 24.99, "stock": 7},
        "3": {"id": 3, "name": "Doohickey C", "price": 4.99, "stock": 100},
    }
    return products.get(pid, {"id": pid, "name": "Unknown", "price": 0, "stock": 0})


@ft.component
def Home():
    data = ft.use_route_loader_data()
    return ft.Column(
        [
            ft.Text(data["title"], size=24),
            ft.Text(data["message"]),
        ]
    )


@ft.component
def ProductsList():
    data = ft.use_route_loader_data()
    return ft.Column(
        [
            ft.Text("Products", size=24),
            *[
                ft.ListTile(
                    title=ft.Text(p["name"]),
                    subtitle=ft.Text(f"${p['price']:.2f}"),
                    on_click=lambda _, pid=p["id"]: ft.context.page.navigate(
                        f"/products/{pid}"
                    ),
                )
                for p in data["products"]
            ],
        ]
    )


@ft.component
def ProductDetails():
    data = ft.use_route_loader_data()
    params = ft.use_route_params()
    return ft.Column(
        [
            ft.Text(data["name"], size=24),
            ft.Text(f"Price: ${data['price']:.2f}"),
            ft.Text(f"In stock: {data['stock']}"),
            ft.Text(f"Product ID (from params): {params['pid']}"),
            ft.Button(
                "Back to products",
                on_click=lambda: ft.context.page.navigate("/products"),
            ),
        ]
    )


@ft.component
def App():
    return ft.Column(
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
            ft.Divider(),
            ft.Router(
                [
                    ft.Route(index=True, component=Home, loader=home_loader),
                    ft.Route(
                        path="products",
                        children=[
                            ft.Route(
                                index=True,
                                component=ProductsList,
                                loader=products_loader,
                            ),
                            ft.Route(
                                path=":pid",
                                component=ProductDetails,
                                loader=product_detail_loader,
                            ),
                        ],
                    ),
                ]
            ),
        ]
    )


ft.run(lambda page: page.render(App))

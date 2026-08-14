import flet as ft

PRODUCTS = [
    {"name": "Desk Lamp", "price": "$24", "on_sale": False},
    {"name": "Wireless Mouse", "price": "$18", "on_sale": True},
    {"name": "Notebook", "price": "$6", "on_sale": False},
]


def main(page: ft.Page):
    page.title = "Catalog"
    page.appbar = ft.AppBar(title=ft.Text("Catalog"), center_title=True)

    def add_to_cart(product_name: str):
        def handle_click(e: ft.Event[ft.Button]):
            page.show_dialog(ft.SnackBar(ft.Text(f"Added {product_name} to cart")))

        return handle_click

    def product_card(product: dict) -> ft.Control:
        card = ft.Container(
            padding=12,
            border_radius=8,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Column(
                        spacing=2,
                        controls=[
                            ft.Text(product["name"], weight=ft.FontWeight.BOLD),
                            ft.Text(product["price"], color=ft.Colors.OUTLINE),
                        ],
                    ),
                    ft.Button("Buy", on_click=add_to_cart(product["name"])),
                ],
            ),
        )
        if not product["on_sale"]:
            return card
        return ft.Stack(
            clip_behavior=ft.ClipBehavior.NONE,
            controls=[
                card,
                ft.Container(
                    content=ft.Text("SALE", size=10, color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.RED,
                    padding=ft.Padding.symmetric(horizontal=6, vertical=2),
                    border_radius=4,
                    top=-6,
                    right=-6,
                ),
            ],
        )

    page.add(
        ft.Column(
            spacing=10,
            controls=[product_card(product) for product in PRODUCTS],
        ),
    )


if __name__ == "__main__":
    ft.run(main)

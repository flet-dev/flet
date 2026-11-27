import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent Flyout"

    def open_flyout(e: ft.Event[fluent.Button]):
        flyout.open = True

    def empty_cart(e: ft.Event[fluent.Button]):
        flyout.open = False
        cart.value = "Your cart is empty"
        empty_button.disabled = True

    cart = ft.Text("3 items in your cart")
    empty_button = fluent.Button("Empty cart", on_click=open_flyout)
    flyout = fluent.Flyout(
        content=empty_button,
        flyout=ft.Column(
            tight=True,
            width=240,
            controls=[
                ft.Text("All items will be removed. Do you want to continue?"),
                fluent.Button("Yes, empty my cart", on_click=empty_cart),
            ],
        ),
    )

    page.add(ft.SafeArea(content=ft.Column(controls=[cart, flyout])))


if __name__ == "__main__":
    ft.run(main)

import random

import flet as ft


def main(page: ft.Page):
    message = ft.Text()
    dd = ft.DropdownM2(options=[], options_fill_horizontally=True)

    def handle_dropdown_change(e: ft.Event[ft.DropdownM2]):
        message.value = f"{e.control.value} chosen"

    def handle_new_random_item(_: ft.Event[ft.Button]):
        icon = ft.Icon(ft.Icons.random())
        dd.options.append(
            ft.dropdownm2.Option(
                text=f"{str(icon.icon)[6:]}",
                content=icon,
            )
        )
        dd.update()

    def handle_items_shuffle(_: ft.Event[ft.Button]):
        random.shuffle(dd.options)
        dd.update()

    dd.on_change = handle_dropdown_change

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    dd,
                    ft.Button("Add random Option", on_click=handle_new_random_item),
                    ft.Button("Shuffle Options", on_click=handle_items_shuffle),
                    message,
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)

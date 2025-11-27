import random

import flet as ft


def main(page: ft.Page):
    def handle_dropdown_change(e: ft.Event[ft.DropdownM2]):
        message.value = f"{e.control.value} chosen"
        page.update()

    def handle_new_random_item(e: ft.Event[ft.Button]):
        icon = ft.Icon(ft.Icons.random())
        dd.options.append(
            ft.dropdownm2.Option(text=f"{str(icon.icon)[6:]}", content=icon)
        )
        page.update()

    def handle_items_shuffle(e: ft.Event[ft.Button]):
        random.shuffle(dd.options)
        page.update()

    page.add(
        dd := ft.DropdownM2(
            options=[], options_fill_horizontally=True, on_change=handle_dropdown_change
        ),
        ft.Button("Add random Option", on_click=handle_new_random_item),
        ft.Button("Shuffle Options", on_click=handle_items_shuffle),
        message := ft.Text(),
    )


if __name__ == "__main__":
    ft.run(main)

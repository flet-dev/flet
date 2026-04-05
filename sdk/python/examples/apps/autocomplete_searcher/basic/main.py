import flet as ft

NAMES = [
    "Adam",
    "William",
    "Emma",
    "Alexander",
    "Julia",
    "Elias",
    "Hugo",
    "Alice",
    "Emil",
    "Anton",
    "Ebba",
    "Elin",
    "Oliver",
    "Axel",
    "Maja",
    "Ella",
    "Alva",
    "Liam",
    "Albin",
    "Elsa",
    "Erik",
    "Ida",
    "Oscar",
    "Wilma",
]


def main(page: ft.Page):
    page.title = "Autocomplete search names"

    def textbox_changed(string):
        str_lower = string.control.value.lower()
        list_view.controls = (
            [list_items.get(n) for n in NAMES if str_lower in n.lower()]
            if str_lower
            else []
        )

    list_items = {
        name: ft.ListTile(
            title=ft.Text(name),
            leading=ft.Icon(ft.Icons.ACCESSIBILITY),
        )
        for name in NAMES
    }

    text_field = ft.TextField(label="Search name:", on_change=textbox_changed)
    list_view = ft.ListView(expand=1, spacing=10, padding=20)

    page.add(
        ft.SafeArea(
            content=ft.Column(
                expand=True,
                controls=[text_field, list_view],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)

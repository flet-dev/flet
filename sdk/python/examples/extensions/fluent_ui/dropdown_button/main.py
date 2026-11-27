import flet_fluent_ui as fluent

import flet as ft

FILES = [
    ("Budget.xlsx", "May 12", 48),
    ("Notes.txt", "May 20", 2),
    ("Photos.zip", "April 30", 2100),
]


def main(page: ft.Page):
    page.title = "Fluent DropDownButton"

    def sort_files(e: ft.Event[fluent.MenuFlyoutItem]):
        for item in sort_button.items:
            item.selected = item is e.control
        sort_button.content = f"Sort by: {e.control.content}"
        show_files(e.control.data)

    def show_files(sort_key):
        files.controls = [
            ft.Text(f"{name}  ·  {modified}  ·  {size} KB")
            for name, modified, size in sorted(FILES, key=sort_key)
        ]

    sort_button = fluent.DropDownButton(
        "Sort by: Name",
        key="sort",
        leading=fluent.FluentIcons.ARROW_SORT,
        items=[
            fluent.MenuFlyoutItem(
                "Name",
                selected=True,
                data=lambda f: f[0],
                on_click=sort_files,
            ),
            fluent.MenuFlyoutItem(
                "Size",
                data=lambda f: f[2],
                on_click=sort_files,
            ),
        ],
    )
    files = ft.Column()
    show_files(lambda f: f[0])

    page.add(ft.SafeArea(content=ft.Column(controls=[sort_button, files])))


if __name__ == "__main__":
    ft.run(main)

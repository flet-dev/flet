import flet_fluent_ui as fluent

import flet as ft

FOLDERS = {
    "Home": ["Documents", "Pictures"],
    "Documents": ["Invoices", "Letters"],
    "Pictures": ["Holidays"],
    "Invoices": [],
    "Letters": [],
    "Holidays": [],
}


def main(page: ft.Page):
    page.title = "Fluent BreadcrumbBar"

    def show(path: list[str]):
        bar.items = [fluent.BreadcrumbItem(name, on_click=go_to) for name in path]
        subfolders.controls = [
            fluent.HyperlinkButton(name, data=name, on_click=open_folder)
            for name in FOLDERS[path[-1]]
        ] or [ft.Text("No subfolders")]

    def path() -> list[str]:
        return [item.content for item in bar.items]

    def go_to(e: ft.Event[fluent.BreadcrumbItem]):
        current = path()
        show(current[: current.index(e.control.content) + 1])

    def open_folder(e: ft.Event[fluent.HyperlinkButton]):
        show([*path(), e.control.data])

    bar = fluent.BreadcrumbBar()
    subfolders = ft.Row()
    show(["Home", "Documents", "Invoices"])

    page.add(ft.SafeArea(content=ft.Column(controls=[bar, subfolders])))


if __name__ == "__main__":
    ft.run(main)

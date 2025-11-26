import flet as ft


def main(page: ft.Page):
    page.add(ft.Text(f"Initial route: {page.route}"))

    def route_change(e):
        page.add(ft.Text(f"New route: {e.route}"))

    page.on_route_change = route_change
    page.update()


if __name__ == "__main__":
    ft.run(main)

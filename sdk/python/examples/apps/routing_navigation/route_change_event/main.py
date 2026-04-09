import flet as ft


def main(page: ft.Page):
    route_log = ft.Column(controls=[ft.Text(f"Initial route: {page.route}")])
    page.add(ft.SafeArea(content=route_log))

    def route_change(e):
        route_log.controls.append(ft.Text(f"New route: {e.route}"))

    page.on_route_change = route_change
    page.update()


if __name__ == "__main__":
    ft.run(main)

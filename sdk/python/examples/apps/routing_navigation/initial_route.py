import flet as ft


def main(page: ft.Page):
    page.add(ft.Text(f"Initial route: {page.route}"))


if __name__ == "__main__":
    ft.run(main)

import flet as ft


def main(page: ft.Page):
    page.add(
        ft.TextField(
            label="Standard",
            multiline=True,
        ),
        ft.TextField(
            label="Disabled",
            multiline=True,
            disabled=True,
            value="line1\nline2\nline3\nline4\nline5",
        ),
        ft.TextField(
            label="Auto adjusted height with max lines",
            multiline=True,
            min_lines=1,
            max_lines=3,
        ),
    )


if __name__ == "__main__":
    ft.run(main)

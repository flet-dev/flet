import flet as ft


def main(page: ft.Page):
    page.add(
        ft.CupertinoCheckbox(label="Cupertino Checkbox", value=True),
        ft.Checkbox(label="Material Checkbox", value=True),
        ft.Container(height=20),
        ft.Text(
            value="Adaptive Checkbox shows as CupertinoCheckbox on macOS and iOS and as Checkbox on other platforms:"
        ),
        ft.Checkbox(adaptive=True, label="Adaptive Checkbox", value=True),
    )


if __name__ == "__main__":
    ft.run(main)

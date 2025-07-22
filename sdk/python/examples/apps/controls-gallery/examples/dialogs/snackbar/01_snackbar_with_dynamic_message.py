import flet as ft

name = "SnackBar with dynamic message"


def example():
    class Data:
        def __init__(self) -> None:
            self.counter = 0

    d = Data()

    def on_click(e):
        # e.control.page.snack_bar = ft.SnackBar(ft.Text(f"Hello {d.counter}"))
        # e.control.page.snack_bar.open = True
        snackbar = ft.SnackBar(ft.Text(f"Hello {d.counter}"))
        e.control.page.overlay.append(snackbar)
        snackbar.open = True
        d.counter += 1
        e.control.page.update()

    return ft.ElevatedButton("Open SnackBar", on_click=on_click)

import flet as ft

name = "Simple BottomSheet"


def example():
    class Example(ft.ElevatedButton):
        def __init__(self):
            super().__init__()
            self.content = "Display bottom sheet"
            self.on_click = self.show_bs
            self.bs = ft.BottomSheet(
                ft.Container(
                    ft.Column(
                        [
                            ft.Text("This is sheet's content!"),
                            ft.ElevatedButton(
                                "Close bottom sheet", on_click=self.close_bs
                            ),
                        ],
                        tight=True,
                    ),
                    padding=10,
                ),
                open=False,
                on_dismiss=self.bs_dismissed,
            )

        def bs_dismissed(self, e):
            print("Dismissed!")

        def show_bs(self, e):
            self.page.show_dialog(self.bs)

        def close_bs(self, e):
            self.page.pop_dialog()

    bs_example = Example()

    return bs_example

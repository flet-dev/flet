import flet as ft

name = """AutoComplete example"""


def example():
    return ft.Column(
        [
            ft.AutoComplete(
                suggestions=[
                    ft.AutoCompleteSuggestion(key="one 1", value="One"),
                    ft.AutoCompleteSuggestion(key="two 2", value="Two"),
                    ft.AutoCompleteSuggestion(key="three 3", value="Three"),
                ],
                on_select=lambda e: print(e.control.selected_index),
            ),
            ft.Text("Type in 1, 2 or 3 to receive suggestions."),
        ]
    )

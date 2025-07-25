import flet as ft

name = """AutoComplete with different properties"""


def example():
    autocomplete = ft.AutoComplete(
        suggestions=[
            ft.AutoCompleteSuggestion(key="four 4", value="Four"),
            ft.AutoCompleteSuggestion(key="five 5", value="Five"),
            ft.AutoCompleteSuggestion(key="six 6", value="Six"),
        ],
        suggestions_max_height=30,
        opacity=0.5,
        visible=True,
        data="data",
        on_select=lambda e: print(e.control.selected_index, e.selection),
    )

    return ft.Column(
        [
            autocomplete,
            ft.Text("Type in 4, 5 or 6 to receive suggestions."),
        ]
    )

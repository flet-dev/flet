import flet as ft

numbers = [
    ("one 1", "One"),
    ("two 2", "Two"),
    ("three 3", "Three"),
    ("four 4", "Four"),
    ("five 5", "Five"),
    ("six 6", "Six"),
    ("seven 7", "Seven"),
    ("eight 8", "Eight"),
    ("nine 9", "Nine"),
    ("ten 10", "Ten"),
]


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def handle_change(e: ft.Event[ft.AutoComplete]):
        info.value = f"Current input 👀: {e.data!r} \n"

    def handle_select(e: ft.AutoCompleteSelectEvent):
        info.value = (
            f"Current input 👀: {e.control.value!r} \n"
            f"Your selection: {e.selection.value}"
        )

    page.add(
        ft.AutoComplete(
            value="One",
            width=200,
            on_change=handle_change,
            on_select=handle_select,
            suggestions=[
                ft.AutoCompleteSuggestion(key=key, value=value)
                for key, value in numbers
            ],
        ),
        info := ft.Text("Enter a number (in words or digits) to get suggestions."),
    )


ft.run(main)

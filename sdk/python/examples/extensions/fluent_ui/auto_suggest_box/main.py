import flet_fluent_ui as fluent

import flet as ft

CITIES = ["Amsterdam", "Athens", "Berlin", "Lisbon", "London", "Madrid", "Paris"]


def main(page: ft.Page):
    page.title = "Fluent AutoSuggestBox"

    def handle_select(e: ft.Event[fluent.AutoSuggestBox]):
        status.value = f"Destination: {e.data}"

    status = ft.Text("Where to?")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                width=300,
                controls=[
                    fluent.AutoSuggestBox(
                        key="city",
                        placeholder="Search a city",
                        prefix=fluent.FluentIcons.SEARCH,
                        on_select=handle_select,
                        items=[
                            fluent.AutoSuggestBoxItem(value=city) for city in CITIES
                        ],
                    ),
                    status,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)

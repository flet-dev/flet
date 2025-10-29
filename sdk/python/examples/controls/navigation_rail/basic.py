import flet as ft


def main(page: ft.Page):
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        group_alignment=-0.9,
        on_change=lambda e: print("Selected destination:", e.control.selected_index),
        leading=ft.FloatingActionButton(
            icon=ft.Icons.CREATE,
            content="Add",
            on_click=lambda e: print("FAB clicked!"),
        ),
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.FAVORITE_BORDER,
                selected_icon=ft.Icons.FAVORITE,
                label="First",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icon(ft.Icons.BOOKMARK_BORDER),
                selected_icon=ft.Icon(ft.Icons.BOOKMARK),
                label="Second",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SETTINGS_OUTLINED,
                selected_icon=ft.Icon(ft.Icons.SETTINGS),
                label=ft.Text("Settings"),
            ),
        ],
    )

    page.add(
        ft.Row(
            expand=True,
            controls=[
                ft.SelectionArea(content=rail),
                ft.VerticalDivider(width=1),
                ft.Column(
                    alignment=ft.MainAxisAlignment.START,
                    expand=True,
                    controls=[ft.Text("Body!")],
                ),
            ],
        )
    )


ft.run(main)

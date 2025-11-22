import flet as ft

name = "Badges in NavigationRail example"


def example():
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        leading=ft.FloatingActionButton(icon=ft.Icons.CREATE, content="Add"),
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icon(ft.Icons.PHONE, badge="10"),
                label="Calls",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icon(ft.Icons.MAIL, badge=ft.Badge()),
                label="Mail",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SETTINGS_OUTLINED,
                selected_icon=ft.Icon(ft.Icons.SETTINGS),
                label=ft.Text("Settings"),
            ),
        ],
        on_change=lambda e: print("Selected destination:", e.control.selected_index),
    )

    return ft.Row(
        [
            rail,
            ft.VerticalDivider(width=1),
            ft.Column(
                [ft.Text("Body!")], alignment=ft.MainAxisAlignment.START, expand=True
            ),
        ],
        width=400,
        height=400,
    )

import flet as ft

name = "Tabs example"


def example():
    return ft.Tabs(
        selected_index=1,
        animation_duration=300,
        tabs=[
            ft.Tab(
                label="Tab 1",
                content=ft.Container(
                    content=ft.Text("This is Tab 1"), alignment=ft.Alignment.CENTER
                ),
            ),
            ft.Tab(
                label=ft.Icon(ft.Icons.SEARCH),
                content=ft.Text("This is Tab 2"),
            ),
            ft.Tab(
                label="Tab 3",
                icon=ft.Icons.SETTINGS,
                content=ft.Text("This is Tab 3"),
            ),
        ],
        width=400,
        height=400,
    )

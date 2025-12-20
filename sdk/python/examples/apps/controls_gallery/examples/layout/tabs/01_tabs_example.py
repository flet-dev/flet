import flet as ft

name = "Tabs example"


def example():
    return ft.Tabs(
        selected_index=1,
        length=3,
        animation_duration=300,
        content=ft.Column(
            controls=[
                ft.TabBar(
                    tabs=[
                        ft.Tab(label="Tab 1"),
                        ft.Tab(
                            label=ft.Icon(ft.Icons.SEARCH),
                        ),
                        ft.Tab(
                            label="Tab 3",
                            icon=ft.Icons.SETTINGS,
                        ),
                    ]
                ),
                ft.TabBarView(
                    controls=[
                        ft.Container(
                            content=ft.Text("This is Tab 1"),
                            alignment=ft.Alignment.CENTER,
                        ),
                        ft.Container(
                            content=ft.Text("This is Tab 2"),
                            alignment=ft.Alignment.CENTER,
                        ),
                        ft.Container(
                            content=ft.Text("This is Tab 3"),
                            alignment=ft.Alignment.CENTER,
                        ),
                    ]
                ),
            ]
        ),
    )

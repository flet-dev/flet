import flet as ft


def main(page: ft.Page):
    page.add(
        ft.Tabs(
            length=2,
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.TabBar(
                        tabs=[
                            ft.Tab(label=ft.Text("Main Tab 1")),
                            ft.Tab(label=ft.Text("Main Tab 2")),
                        ],
                    ),
                    ft.TabBarView(
                        expand=True,
                        controls=[
                            ft.Tabs(
                                length=2,
                                expand=True,
                                content=ft.Column(
                                    expand=True,
                                    controls=[
                                        ft.TabBar(
                                            secondary=True,
                                            tabs=[
                                                ft.Tab(label=ft.Text("SubTab 1")),
                                                ft.Tab(label=ft.Text("SubTab 2")),
                                            ],
                                        ),
                                        ft.TabBarView(
                                            expand=True,
                                            controls=[
                                                ft.Text("Nested Tab 1 content"),
                                                ft.Text("Nested Tab 2 content"),
                                            ],
                                        ),
                                    ],
                                ),
                            ),
                            ft.Text("Main Tab 1 content"),
                        ],
                    ),
                ],
            ),
        )
    )


ft.run(main)

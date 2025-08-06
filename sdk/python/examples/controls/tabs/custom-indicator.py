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
                        tab_alignment=ft.TabAlignment.START,
                        indicator_animation=ft.TabIndicatorAnimation.ELASTIC,
                        indicator_size=ft.TabBarIndicatorSize.LABEL,
                        indicator=ft.UnderlineTabIndicator(
                            border_side=ft.BorderSide(5, color=ft.Colors.RED),
                            border_radius=ft.BorderRadius.all(1),
                            insets=ft.Padding.only(bottom=5),
                        ),
                        # indicator_thickness=5,
                        # indicator_color=ft.Colors.RED,
                        tabs=[
                            ft.Tab(label=ft.Text("Home")),
                            ft.Tab(label=ft.Text("My Account")),
                        ],
                    ),
                    ft.TabBarView(
                        expand=True,
                        controls=[
                            ft.Text("Home Tab Content"),
                            ft.Text("Profile Tab Content"),
                        ],
                    ),
                ],
            ),
        )
    )


ft.run(main)

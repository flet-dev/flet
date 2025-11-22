import flet as ft

name = "Customize Tabs theme"


def example():
    t = ft.Tabs(
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

    c = ft.Container(
        content=t,
        height=300,
        width=300,
        border=ft.Border.all(1, "black"),
        theme=ft.Theme(
            tab_bar_theme=ft.TabBarTheme(
                divider_color=ft.Colors.BLUE,
                indicator_color=ft.Colors.RED,
                label_color=ft.Colors.GREEN,
                unselected_label_color=ft.Colors.AMBER,
                overlay_color={
                    ft.ControlState.FOCUSED: ft.Colors.with_opacity(
                        0.2, ft.Colors.GREEN
                    ),
                    ft.ControlState.DEFAULT: ft.Colors.with_opacity(
                        0.2, ft.Colors.PINK
                    ),
                },
            )
        ),
    )

    return c

import flet as ft

name = "Customize Tabs theme"


def example():
    t = ft.Tabs(
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
        expand=1,
    )

    c = ft.Container(
        content=t,
        height=300,
        width=300,
        border=ft.Border.all(1, "black"),
        theme=ft.Theme(
            tabs_theme=ft.TabsTheme(
                divider_color=ft.Colors.BLUE,
                indicator_color=ft.Colors.RED,
                indicator_tab_size=True,
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

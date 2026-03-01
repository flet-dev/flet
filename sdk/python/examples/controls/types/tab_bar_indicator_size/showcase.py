import flet as ft


def showcase_card(indicator_size: ft.TabBarIndicatorSize) -> ft.Container:
    tabs_count = 3

    tab_bar = ft.TabBar(
        indicator_size=indicator_size,
        indicator=ft.UnderlineTabIndicator(
            border_side=ft.BorderSide(width=4, color=ft.Colors.PRIMARY),
            insets=ft.Padding.only(bottom=3),
        ),
        tabs=[
            ft.Tab(label="A"),
            ft.Tab(label="Long Label"),
            ft.Tab(label="Mid"),
        ],
    )

    tab_view = ft.Container(
        height=70,
        alignment=ft.Alignment.CENTER,
        border=ft.Border.all(1, ft.Colors.OUTLINE),
        border_radius=8,
        bgcolor=ft.Colors.SURFACE,
        content=ft.TabBarView(
            controls=[
                ft.Container(
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text(f"View {i + 1}"),
                )
                for i in range(tabs_count)
            ]
        ),
    )

    return ft.Container(
        width=380,
        padding=12,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(indicator_size.name, weight=ft.FontWeight.BOLD),
                ft.Tabs(
                    length=tabs_count,
                    selected_index=1,
                    content=ft.Column(spacing=8, controls=[tab_bar, tab_view]),
                ),
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="TabBarIndicatorSize Showcase")
    page.add(
        ft.Text("Compare indicator width when matching tab bounds vs label bounds."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                showcase_card(indicator_size)
                for indicator_size in ft.TabBarIndicatorSize
            ],
        ),
    )


ft.run(main)

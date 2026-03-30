import flet as ft


def showcase_card(alignment: ft.TabAlignment) -> ft.Container:
    scrollable = alignment != ft.TabAlignment.FILL
    tabs_count = 4

    tab_bar = ft.TabBar(
        scrollable=scrollable,
        tab_alignment=alignment,
        tabs=[ft.Tab(label=f"Tab {i + 1}") for i in range(tabs_count)],
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
                ft.Text(alignment.name, weight=ft.FontWeight.BOLD),
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

    page.appbar = ft.AppBar(title="TabAlignment Showcase")
    page.add(
        ft.Text("Compare how tabs are positioned within the tab bar."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(alignment) for alignment in ft.TabAlignment],
        ),
    )


ft.run(main)

import flet as ft


def showcase_card(mode: ft.OverlayVisibilityMode) -> ft.Container:
    return ft.Container(
        width=380,
        padding=12,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(mode.name, weight=ft.FontWeight.BOLD),
                ft.Text("Prefix/suffix visibility (prefilled):", size=11),
                ft.CupertinoTextField(
                    value="Flet",
                    placeholder_text="Search",
                    prefix=ft.Icon(ft.CupertinoIcons.SEARCH),
                    suffix=ft.Icon(ft.CupertinoIcons.MIC),
                    prefix_visibility_mode=mode,
                    suffix_visibility_mode=mode,
                ),
                ft.Text("Clear button visibility:", size=11),
                ft.CupertinoTextField(
                    value="Clear me",
                    placeholder_text="Type text",
                    clear_button_visibility_mode=mode,
                ),
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="OverlayVisibilityMode Showcase")
    page.add(
        ft.Text("Compare when Cupertino text field overlays appear."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(mode) for mode in ft.OverlayVisibilityMode],
        ),
    )


ft.run(main)

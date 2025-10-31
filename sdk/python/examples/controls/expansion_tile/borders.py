import flet as ft


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT

    page.add(
        ft.ExpansionTile(
            title=ft.Text(
                value="Expansion Tile with changing borders",
                text_align=ft.TextAlign.CENTER,
            ),
            subtitle=ft.Text(
                value="Tile border changes when expanded",
                text_align=ft.TextAlign.CENTER,
            ),
            bgcolor=ft.Colors.BLUE_GREY_200,
            controls_padding=ft.Padding.symmetric(horizontal=10),
            collapsed_bgcolor=ft.Colors.BLUE_GREY_200,
            affinity=ft.TileAffinity.PLATFORM,
            maintain_state=True,
            shape=ft.RoundedRectangleBorder(radius=20),
            collapsed_shape=ft.StadiumBorder(side=ft.BorderSide(width=2)),
            collapsed_text_color=ft.Colors.GREY_800,
            text_color=ft.Colors.GREY_800,
            controls=[
                ft.ListTile(
                    title=ft.Text("A sub-tile"),
                    bgcolor=ft.Colors.BLUE_GREY_200,
                    shape=ft.RoundedRectangleBorder(radius=20),
                    # shape=ft.StadiumBorder(),
                ),
                ft.ListTile(
                    title=ft.Text("Another sub-tile"),
                    bgcolor=ft.Colors.BLUE_GREY_200,
                    shape=ft.RoundedRectangleBorder(radius=20),
                    # shape=ft.StadiumBorder(),
                ),
            ],
        ),
    )


if __name__ == "__main__":
    ft.run(main)

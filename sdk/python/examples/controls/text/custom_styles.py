import flet as ft


def main(page: ft.Page):
    page.title = "Text custom styles"
    page.scroll = ft.ScrollMode.ADAPTIVE

    page.add(
        ft.Text("Size 10", size=10),
        ft.Text("Size 30, Italic", size=30, color=ft.Colors.PINK_600, italic=True),
        ft.Text(
            value="Size 40, w100",
            size=40,
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE_600,
            weight=ft.FontWeight.W_100,
        ),
        ft.Text(
            value="Size 50, Normal",
            size=50,
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.ORANGE_800,
            weight=ft.FontWeight.NORMAL,
        ),
        ft.Text(
            value="Size 60, Bold, Italic",
            size=50,
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.GREEN_700,
            weight=ft.FontWeight.BOLD,
            italic=True,
        ),
        ft.Text(
            value="Size 70, w900, selectable",
            size=70,
            weight=ft.FontWeight.W_900,
            selectable=True,
        ),
        ft.Text(
            value="Limit long text to 1 line with ellipsis",
            theme_style=ft.TextThemeStyle.HEADLINE_SMALL,
        ),
        ft.Text(
            value="Proin rutrum, purus sit amet elementum volutpat, nunc lacus vulputate orci, cursus ultrices neque dui quis purus. Ut ultricies purus nec nibh bibendum, eget vestibulum metus various. Duis convallis maximus justo, eu rutrum libero maximus id. Donec ullamcorper arcu in sapien molestie, non pellentesque tellus pellentesque. Nulla nec tristique ex. Maecenas euismod nisl enim, a convallis arcu laoreet at. Ut at tortor finibus, rutrum massa sit amet, pulvinar velit. Phasellus diam lorem, viverra vitae leo vitae, consequat suscipit lorem.",
            max_lines=1,
            overflow=ft.TextOverflow.ELLIPSIS,
        ),
        ft.Text(
            value="Limit long text to 2 lines and fading",
            theme_style=ft.TextThemeStyle.HEADLINE_SMALL,
        ),
        ft.Text(
            value="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur quis nibh vitae purus consectetur facilisis sed vitae ipsum. Quisque faucibus sed nulla placerat sagittis. Phasellus condimentum risus vitae nulla vestibulum auctor. Curabitur scelerisque, nibh eget imperdiet consequat, odio ante tempus diam, sed volutpat nisl erat eget turpis. Sed viverra, diam sit amet blandit vulputate, mi tellus dapibus lorem, vitae vehicula diam mauris placerat diam. Morbi sit amet pretium turpis, et consequat ligula. Nulla velit sem, suscipit sit amet dictum non, tincidunt sed nulla. Aenean pellentesque odio porttitor sagittis aliquam. Name various at metus vitae vulputate. Praesent faucibus nibh lorem, eu pretium dolor dictum nec. Phasellus eget dui laoreet, viverra magna vitae, pellentesque diam.",
            max_lines=2,
        ),
        ft.Text(
            value="Limit the width and height of long text",
            theme_style=ft.TextThemeStyle.HEADLINE_SMALL,
        ),
        ft.Text(
            value="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur quis nibh vitae purus consectetur facilisis sed vitae ipsum. Quisque faucibus sed nulla placerat sagittis. Phasellus condimentum risus vitae nulla vestibulum auctor. Curabitur scelerisque, nibh eget imperdiet consequat, odio ante tempus diam, sed volutpat nisl erat eget turpis. Sed viverra, diam sit amet blandit vulputate, mi tellus dapibus lorem, vitae vehicula diam mauris placerat diam. Morbi sit amet pretium turpis, et consequat ligula. Nulla velit sem, suscipit sit amet dictum non, tincidunt sed nulla. Aenean pellentesque odio porttitor sagittis aliquam. Name various at metus vitae vulputate. Praesent faucibus nibh lorem, eu pretium dolor dictum nec. Phasellus eget dui laoreet, viverra magna vitae, pellentesque diam.",
            width=700,
            height=100,
        ),
    )


if __name__ == "__main__":
    ft.run(main)

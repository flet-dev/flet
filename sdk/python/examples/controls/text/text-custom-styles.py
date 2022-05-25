import flet
from flet import Page, Text, colors


def main(page: Page):
    page.title = "Text custom styles"
    page.scroll = "adaptive"

    page.add(
        Text("Size 10", size=10),
        Text("Size 30, Italic", size=20, color="pink600", italic=True),
        Text(
            "Size 40, w100",
            size=40,
            color=colors.WHITE,
            bgcolor=colors.BLUE_600,
            weight="w100",
        ),
        Text(
            "Size 50, Normal",
            size=50,
            color=colors.WHITE,
            bgcolor=colors.ORANGE_800,
            weight="normal",
        ),
        Text(
            "Size 60, Bold, Italic",
            size=50,
            color=colors.WHITE,
            bgcolor=colors.GREEN_700,
            weight="bold",
            italic=True,
        ),
        Text("Size 70, w900, selectable", size=70, weight="w900", selectable=True),
        Text("Limit long text to 1 line with ellipsis", style="headlineSmall"),
        Text(
            "Proin rutrum, purus sit amet elementum volutpat, nunc lacus vulputate orci, cursus ultrices neque dui quis purus. Ut ultricies purus nec nibh bibendum, eget vestibulum metus varius. Duis convallis maximus justo, eu rutrum libero maximus id. Donec ullamcorper arcu in sapien molestie, non pellentesque tellus pellentesque. Nulla nec tristique ex. Maecenas euismod nisl enim, a convallis arcu laoreet at. Ut at tortor finibus, rutrum massa sit amet, pulvinar velit. Phasellus diam lorem, viverra vitae leo vitae, consequat suscipit lorem.",
            max_lines=1,
            overflow="ellipsis",
        ),
        Text("Limit long text to 2 lines and fading", style="headlineSmall"),
        Text(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur quis nibh vitae purus consectetur facilisis sed vitae ipsum. Quisque faucibus sed nulla placerat sagittis. Phasellus condimentum risus vitae nulla vestibulum auctor. Curabitur scelerisque, nibh eget imperdiet consequat, odio ante tempus diam, sed volutpat nisl erat eget turpis. Sed viverra, diam sit amet blandit vulputate, mi tellus dapibus lorem, vitae vehicula diam mauris placerat diam. Morbi sit amet pretium turpis, et consequat ligula. Nulla velit sem, suscipit sit amet dictum non, tincidunt sed nulla. Aenean pellentesque odio porttitor sagittis aliquam. Nam varius at metus vitae vulputate. Praesent faucibus nibh lorem, eu pretium dolor dictum nec. Phasellus eget dui laoreet, viverra magna vitae, pellentesque diam.",
            max_lines=2,
        ),
        Text("Limit the width and height of long text", style="headlineSmall"),
        Text(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur quis nibh vitae purus consectetur facilisis sed vitae ipsum. Quisque faucibus sed nulla placerat sagittis. Phasellus condimentum risus vitae nulla vestibulum auctor. Curabitur scelerisque, nibh eget imperdiet consequat, odio ante tempus diam, sed volutpat nisl erat eget turpis. Sed viverra, diam sit amet blandit vulputate, mi tellus dapibus lorem, vitae vehicula diam mauris placerat diam. Morbi sit amet pretium turpis, et consequat ligula. Nulla velit sem, suscipit sit amet dictum non, tincidunt sed nulla. Aenean pellentesque odio porttitor sagittis aliquam. Nam varius at metus vitae vulputate. Praesent faucibus nibh lorem, eu pretium dolor dictum nec. Phasellus eget dui laoreet, viverra magna vitae, pellentesque diam.",
            width=700,
            height=100,
        ),
    )


flet.app(target=main)

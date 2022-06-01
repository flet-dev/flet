import flet
from flet import CircleAvatar, Icon, Stack, Text, alignment, colors, icons
from flet.container import Container


def main(page):
    # a "normal" avatar with background image
    a1 = CircleAvatar(
        foreground_image_url="https://avatars.githubusercontent.com/u/5041459?s=88&v=4",
        content=Text("FF"),
    )
    # avatar with failing foregroung image and fallback text
    a2 = CircleAvatar(
        foreground_image_url="https://avatars.githubusercontent.com/u/_5041459?s=88&v=4",
        content=Text("FF"),
    )
    # avatar with icon, aka icon with inverse background
    a3 = CircleAvatar(
        content=Icon(icons.ABC),
    )
    # avatar with icon and custom colors
    a4 = CircleAvatar(
        content=Icon(icons.WARNING_ROUNDED),
        color=colors.YELLOW_200,
        bgcolor=colors.AMBER_700,
    )
    # avatar with online status
    a5 = Stack(
        [
            CircleAvatar(
                foreground_image_url="https://avatars.githubusercontent.com/u/5041459?s=88&v=4"
            ),
            Container(
                content=CircleAvatar(bgcolor=colors.GREEN, radius=5),
                alignment=alignment.bottom_left,
            ),
        ],
        width=40,
        height=40,
    )
    page.add(a1, a2, a3, a4, a5)


flet.app(target=main)

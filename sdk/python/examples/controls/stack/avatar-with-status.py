import flet
from flet import CircleAvatar, Container, Stack, alignment, colors


def main(page):
    # avatar with online status
    page.add(
        Stack(
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
    )


flet.app(target=main)

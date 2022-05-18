import flet
from flet import Image, Page, Row, border_radius


def main(page: Page):
    page.title = "Images Example"
    page.theme_mode = "light"
    page.padding = 50
    page.update()

    img = Image(
        src=f"/icons/icon-512.png",
        width=100,
        height=100,
        fit="contain",
    )
    images = Row(expand=1, wrap=False, scroll="always")

    page.add(img, images)

    for i in range(0, 30):
        images.controls.append(
            Image(
                src=f"https://picsum.photos/200/200?{i}",
                width=200,
                height=200,
                fit="none",
                repeat="noRepeat",
                border_radius=border_radius.all(10),
            )
        )
    page.update()


flet.app(target=main)

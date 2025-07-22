import flet
from flet import ElevatedButton, Page, colors, icons
from flet_toasts import Toast


def main(page: Page):
    btn = ElevatedButton("Toast")
    page.add(btn)
    Toast(
        page,
        icons.PERSON_SHARP,
        "Toast title",
        "Toast description",
        btn,
        colors.WHITE,
    ).struct()


if __name__ == "__main__":
    flet.app(target=main)

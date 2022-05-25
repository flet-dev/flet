import flet
from flet import GridView, Image, Page, border_radius


def main(page: Page):
    page.title = "GridView Example"
    page.theme_mode = "dark"
    page.padding = 50
    page.update()

    images = GridView(
        expand=1,
        runs_count=5,
        max_extent=150,
        child_aspect_ratio=1.0,
        spacing=5,
        run_spacing=5,
    )

    page.add(images)

    for i in range(0, 60):
        images.controls.append(
            Image(
                src=f"https://picsum.photos/150/150?{i}",
                fit="none",
                repeat="noRepeat",
                border_radius=border_radius.all(10),
            )
        )
    page.update()


flet.app(target=main)

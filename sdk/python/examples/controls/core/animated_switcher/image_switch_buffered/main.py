import base64
import time
from dataclasses import field

import httpx

import flet as ft


@ft.control
class BufferingSwitcher(ft.AnimatedSwitcher):
    content: ft.Image | None = None
    image_queue: list[str] = field(default_factory=list)

    def init(self):
        self.transition = ft.AnimatedSwitcherTransition.SCALE
        self.duration = 500
        self.reverse_duration = 100
        self.switch_in_curve = ft.AnimationCurve.EASE_IN
        self.switch_out_curve = ft.AnimationCurve.EASE_OUT
        if self.content and self.content.src:
            self.image_queue.append(self.content.src)

    def animate(self, e):
        self.content = ft.Image(
            src=self.image_queue.pop(),
            width=200,
            height=300,
            gapless_playback=True,
        )
        self.update()

    async def fill_queue(self):
        while len(self.image_queue) < 10:
            image_base64 = await self.image_to_base64(
                f"https://picsum.photos/200/300?{time.time()}"
            )
            if image_base64:
                self.image_queue.append(image_base64)

    async def image_to_base64(self, url):
        response = await httpx.AsyncClient(follow_redirects=True).get(url)
        if response.status_code == 200:
            base64_str = (
                base64.standard_b64encode(response.content).decode("utf-8").strip()
            )
            return base64_str
        else:
            print(f"Image request failed with {response.status_code}")
            return None

    def before_update(self):
        self.page.run_task(self.fill_queue)


def main(page: ft.Page):
    switcher = BufferingSwitcher(
        content=ft.Image(
            src=f"https://picsum.photos/200/300?{time.time()}",
            width=200,
            height=300,
        )
    )

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    switcher,
                    ft.Button("Animate!", on_click=switcher.animate),
                ]
            )
        ),
    )


if __name__ == "__main__":
    ft.run(main)

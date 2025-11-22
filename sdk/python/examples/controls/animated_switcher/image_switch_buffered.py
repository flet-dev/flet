import base64
import time

import httpx

import flet as ft


class BufferingSwitcher(ft.AnimatedSwitcher):
    image_queue = []

    def __init__(self, image: ft.Image):
        super().__init__(image)
        self.transition = ft.AnimatedSwitcherTransition.SCALE
        self.duration = 500
        self.reverse_duration = 100
        self.switch_in_curve = ft.AnimationCurve.EASE_IN
        self.switch_out_curve = ft.AnimationCurve.EASE_OUT
        self.image_queue.append(image)

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
            self.image_queue.append(
                await self.image_to_base64(
                    f"https://picsum.photos/200/300?{time.time()}"
                )
            )

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
        ft.Image(
            src=f"https://picsum.photos/200/300?{time.time()}", width=200, height=300
        )
    )

    page.add(
        switcher,
        ft.Button("Animate!", on_click=switcher.animate),
    )


ft.run(main)

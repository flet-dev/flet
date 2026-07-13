import asyncio
import urllib.request

import flet as ft

PHOTOS = [
    f"https://picsum.photos/seed/{seed}/800/500.jpg"
    for seed in ("flet", "raw", "image", "viewer", "photo")
]


async def main(page: ft.Page):
    page.title = "RawImage photo viewer"

    raw_image = ft.RawImage(expand=True, fit=ft.BoxFit.CONTAIN)
    status_text = ft.Text("", size=12)

    index = 0
    cache: dict[str, bytes] = {}

    async def fetch(url: str) -> bytes:
        if url not in cache:
            cache[url] = await asyncio.to_thread(
                lambda: urllib.request.urlopen(url, timeout=20).read()
            )
        return cache[url]

    async def show(i: int):
        nonlocal index
        index = i % len(PHOTOS)
        status_text.value = f"loading {index + 1}/{len(PHOTOS)}…"
        page.update()
        data = await fetch(PHOTOS[index])
        # render_encoded displays PNG/JPEG/WebP bytes from anywhere: an
        # HTTP response like here, a file (Path("photo.jpg").read_bytes()),
        # a database blob. The client decodes them with its image codecs.
        await raw_image.render_encoded(data)
        status_text.value = f"{index + 1}/{len(PHOTOS)} — {len(data) // 1024} KB JPEG"
        page.update()

    def go(delta: int):
        asyncio.create_task(show(index + delta))

    page.add(
        ft.Row(
            [
                ft.IconButton(ft.Icons.CHEVRON_LEFT, on_click=lambda: go(-1)),
                ft.IconButton(ft.Icons.CHEVRON_RIGHT, on_click=lambda: go(1)),
                status_text,
            ],
            spacing=10,
        ),
        raw_image,
    )
    await show(0)


if __name__ == "__main__":
    ft.run(main)

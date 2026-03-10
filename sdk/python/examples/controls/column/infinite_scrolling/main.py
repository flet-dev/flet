import threading

import flet as ft


class State:
    i = 0


s = State()
sem = threading.Semaphore()


def main(page: ft.Page):
    def on_scroll(e: ft.OnScrollEvent):
        if e.pixels >= e.max_scroll_extent - 100 and sem.acquire(blocking=False):
            try:
                for _i in range(0, 10):
                    cl.controls.append(ft.Text(f"Text line {s.i}", key=str(s.i)))
                    s.i += 1
                cl.update()
            finally:
                sem.release()

    cl = ft.Column(
        spacing=10,
        height=200,
        width=200,
        scroll=ft.ScrollMode.ALWAYS,
        scroll_interval=0,
        on_scroll=on_scroll,
    )
    for _i in range(0, 50):
        cl.controls.append(ft.Text(f"Text line {s.i}", key=str(s.i)))
        s.i += 1

    page.add(ft.Container(cl, border=ft.Border.all(1)))


ft.run(main)

import asyncio
import time

import flet as ft


class CpuProgressApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.loop = asyncio.get_running_loop()

        self.page.title = "Simple thread + asyncio task (Queue)"
        self.pb = ft.ProgressBar(value=0.0, width=420)
        self.btn = ft.Button("Start", on_click=self.start_clicked)
        self.page.add(ft.Column([self.btn, self.pb], tight=True, spacing=10))

        # Async queue for progress updates from the worker
        self.progress_queue: asyncio.Queue[float] = asyncio.Queue(maxsize=100)

        # Start one consumer task that keeps the UI in sync with queue updates
        self.consumer_task = asyncio.create_task(self.consume_progress())

    # ---------- Queue consumer (runs on main asyncio loop) ----------
    async def consume_progress(self):
        while True:
            p = await self.progress_queue.get()  # 0..1
            self.pb.value = p
            self.page.update()

    # ---------- Enqueue helper usable from any thread ----------
    def enqueue_progress(self, p: float):
        # Called from the worker thread; schedule a put into the asyncio queue
        asyncio.run_coroutine_threadsafe(self.progress_queue.put(p), self.loop)

    # ---------- Click handler ----------
    async def start_clicked(self, _=None):
        self.btn.disabled = True
        await self.progress_queue.put(0.0)

        # Run blocking job in a thread and wait for it to finish
        await asyncio.to_thread(self.long_job, 100, self.enqueue_progress)

        self.btn.disabled = False
        await self.progress_queue.put(1.0)  # final update

    # ---------- Blocking job (runs in thread) ----------
    @staticmethod
    def long_job(steps: int, enqueue_progress):
        for i in range(steps):
            _ = sum(range(200_000))  # small CPU burn; bump if needed
            time.sleep(0.1)
            enqueue_progress((i + 1) / steps)  # 0..1


if __name__ == "__main__":
    ft.run(CpuProgressApp)

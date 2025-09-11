import asyncio
import time

import flet as ft


class CpuProgressApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.loop = asyncio.get_running_loop()

        self.page.title = "Simple thread + asyncio task"
        self.pb = ft.ProgressBar(value=0.0, width=420)
        self.btn = ft.Button("Start", on_click=self.start_clicked)
        self.page.add(ft.Column([self.btn, self.pb], tight=True, spacing=10))

    # ---------- Thread-safe UI updates ----------
    async def set_progress(self, p: float):
        self.pb.value = p
        self.page.update()

    def report_callback(self, p: float):
        # Called from worker thread -> hop to main asyncio loop
        asyncio.run_coroutine_threadsafe(self.set_progress(p), self.loop)

    # ---------- Handlers ----------
    async def start_clicked(self, _=None):
        self.btn.disabled = True
        await self.set_progress(0.0)

        # Run blocking job in a thread and wait for it to finish
        await asyncio.to_thread(self.long_job, 100, self.report_callback)

        self.btn.disabled = False
        await self.set_progress(1.0)

    # ---------- Blocking job ----------
    @staticmethod
    def long_job(steps: int, report_callback):
        for i in range(steps):
            _ = sum(range(200_000))  # small CPU burn; bump if needed
            time.sleep(0.1)
            report_callback((i + 1) / steps)  # 0..1


if __name__ == "__main__":
    ft.run(CpuProgressApp)

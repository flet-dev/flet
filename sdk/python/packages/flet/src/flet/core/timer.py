import typing
import threading


class Timer:
    """
    It demonstrates how to create a countdown timer using threading for real-time display updates.

    Example:
    ```
    import flet as ft
    from datetime import datetime


    def main(page: ft.Page):
        page.title = "Timer Example"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        page.window.width = 360
        page.window.height = 600

        def update_time():
            timer_txt.value = datetime.now().strftime("%H:%M:%S")
            page.update()

        timer = ft.Timer(callback=update_time)

        timer_txt = ft.Text(
            value=datetime.now().strftime("%H:%M:%S"), 
            text_align="center",
            size=24
        )

        page.add(
            timer_txt,
            ft.Button(
                text = "Start",
                on_click=lambda e: timer.start()
            ),
            ft.Button(
                text = "Stop",
                on_click=lambda e: timer.stop()
            ),
            ft.Button(
                text = "Pause",
                on_click=lambda e: timer.pause()
            ),
            ft.Button(
                text = "Resume",
                on_click=lambda e: timer.resume()
            )
        )

    ft.app(target=main)
    ```
    """

    def __init__(self, 
                 interval: float = 1, 
                 callback: typing.Callable = None, 
                 *args, 
                 **kwargs):

        self.interval = interval
        self.callback = callback
        self.active = False
        self.paused = False
        self.pause_condition = threading.Condition(threading.Lock())
        self.th = threading.Thread(target=self.tick, daemon=True)

    def set_interval(self, interval: float) -> None:
        self.interval = interval

    def set_callback(self, callback: typing.Callable) -> None:
        self.callback = callback

    def start(self):
        self.active = True
        self.paused = False
        if not self.th.is_alive():
            self.th = threading.Thread(target=self.tick, daemon=True)
            self.th.start()

    def stop(self):
        self.active = False
        # Resume if paused to exit the loop
        self.resume()

    def pause(self):
        with self.pause_condition:
            self.paused = True

    def resume(self):
        with self.pause_condition:
            self.paused = False
             # Notify the condition to resume the loop
            self.pause_condition.notify()

    def tick(self):
        while self.active:
            with self.pause_condition:
                while self.paused:
                    # Wait until resume is called
                    self.pause_condition.wait()
            try:
                if self.callback:
                    self.callback()
            except Exception as e:
                print(e)

            threading.Event().wait(self.interval)

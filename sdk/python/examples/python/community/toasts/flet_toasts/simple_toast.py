import threading
import time

from flet import *
from flet import border, colors, icons


class Toast:
    """
    Note: UserControl is not used due to some issues of display

    `Parameters`:
        `page` -> page of main function\n
        `icon` -> icon heading\n
        `msg_title` -> message title\n
        `trigger` -> button that triggers toast\n
        `bgcolor` -> container background color\n
        `auto_close` -> closes in `auto_close` seconds

    TODOS:
        TODO: Implement timer
        TODO: Implement different types. `Success`, `Info`, `Danger`
    """

    def __init__(
        self,
        page: Page,
        icon,
        msg_title,
        msg_desc,
        trigger,
        bgcolor: str = None,
        auto_close: int = 5,
    ):
        self.page = page
        self.icon = icon
        self.msg_title = msg_title
        self.msg_desc = msg_desc
        self.trigger = trigger
        assert hasattr(self.trigger, "on_click"), (
            "Control must contain `on_click` attribute"
        )
        self.trigger.on_click = lambda x: threading.Thread(
            target=self._update_visibility, daemon=True
        ).start()

        self.bgcolor = bgcolor
        self.auto_close = auto_close

    def _update_visibility(self):
        self.stack.opacity = 0 if self.stack.opacity == 1 else 1
        self.page.update()
        time.sleep(self.auto_close)

        if self.stack.opacity == 1:
            threading.Thread(target=self._auto_disapper, daemon=True).start()

    def _auto_disapper(self):
        self.stack.opacity = 0
        self.page.update()

    def _close(self):
        self.stack.opacity = 0
        self.page.update()

    def _start_timer(self):
        pass

    def struct(self):
        main_stack = Stack(expand=True)
        main_stack.controls = [self.toast_container()]
        self.page.add(main_stack)

    def toast_container(self):
        self.timer = 0

        header = Row(
            controls=[
                Row([Icon(self.icon), Text(self.msg_title)]),
                Row(
                    [
                        Text(f"{self.timer} seconds ago"),
                        IconButton(
                            icons.CLOSE_OUTLINED,
                            on_click=lambda x: threading.Thread(
                                target=self._close, daemon=True
                            ).start(),
                        ),
                    ]
                ),
            ],
            alignment="spaceBetween",
        )

        toast_content = Text(self.msg_desc)

        self.container = Container(
            content=Column([header, Divider(), toast_content]),
            width=400,
            bgcolor=self.bgcolor,
            border_radius=10,
            padding=10,
            border=border.all(0.5, colors.BLACK12),
            right=0,
            bottom=0,
            expand=True,
        )

        self.stack = Stack(
            width=self.page.window_width,
            height=self.page.window_height,
            controls=[self.container],
            opacity=0,
            animate_opacity=500,
            expand=True,
        )
        return self.stack

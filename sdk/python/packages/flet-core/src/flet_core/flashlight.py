from typing import Any, Optional

from flet_core.control import Control
from flet_core.ref import Ref


class Flashlight(Control):
    """
    A control to use Flash Light. Works on iOS and Android. Based on torch_light Flutter widget (https://pub.dev/packages/torch_light).

    Flash control is non-visual and should be added to `page.overlay` list.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        flashLight = ft.Flash()
        page.overlay.append(flashLight)
        page.add(
            ft.TextButton("On", on_click:lambda _: flashLight.on()),
            ft.ElevatedButton("Off", on_click:lambda _: flashLight.off()),
        )

    ft.app(target=main)
    ```

    """

    def __init__(
        self,
        ref: Optional[Ref] = None,
        data: Any = None,
    ):
        Control.__init__(
            self,
            ref=ref,
            data=data,
        )

        self.turned_on = False

    def _get_control_name(self):
        return "flashlight"

    def on(self, wait_timeout: Optional[int] = 3) -> int:
        sr = self.invoke_method("on", wait_for_result=True, wait_timeout=wait_timeout)
        self.turned_on = True
        return int(sr)

    def off(self, wait_timeout: Optional[int] = 3) -> int:
        sr = self.invoke_method("off", wait_for_result=True, wait_timeout=wait_timeout)
        self.turned_on = False
        return int(sr)

    def switch(self, wait_timeout: Optional[int] = 3) -> int:
        if self.turned_on:
            return self.off(wait_timeout)
        return self.on(wait_timeout)

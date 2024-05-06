from typing import Any, Optional

from flet_core.control import Control
from flet_core.ref import Ref


class Flash(Control):
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

    def _get_control_name(self):
        return "flash"

    def on(self, wait_timeout: Optional[int] = 3) -> int:
        sr = self.invoke_method("on", wait_for_result=True, wait_timeout=wait_timeout)
        return int(sr)

    def off(self, wait_timeout: Optional[int] = 3) -> int:
        sr = self.invoke_method("off", wait_for_result=True, wait_timeout=wait_timeout)
        return int(sr)

from typing import Any, Optional

from flet_core.control import Control
from flet_core.ref import Ref
from flet_core.utils import deprecated


class HapticFeedback(Control):
    """
    Allows access to the haptic feedback interface on the device.

    It is non-visual and should be added to `page.overlay` list.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        hf = ft.HapticFeedback()
        page.overlay.append(hf)

        page.add(
            ft.ElevatedButton("Heavy impact", on_click=lambda _: hf.heavy_impact()),
            ft.ElevatedButton("Medium impact", on_click=lambda _: hf.medium_impact()),
            ft.ElevatedButton("Light impact", on_click=lambda _: hf.light_impact()),
            ft.ElevatedButton("Vibrate", on_click=lambda _: hf.vibrate()),
        )

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/hapticfeedback
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
        return "hapticfeedback"

    def is_isolated(self):
        return True

    def heavy_impact(self):
        self.invoke_method("heavy_impact")

    @deprecated(
        reason="Use heavy_impact() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def heavy_impact_async(self):
        self.heavy_impact()

    def light_impact(self):
        self.invoke_method("light_impact")

    @deprecated(
        reason="Use light_impact() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def light_impact_async(self):
        self.light_impact()

    def medium_impact(self):
        self.invoke_method("medium_impact")

    @deprecated(
        reason="Use medium_impact() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def medium_impact_async(self):
        self.medium_impact()

    def vibrate(self):
        self.invoke_method("vibrate")

    @deprecated(
        reason="Use vibrate() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def vibrate_async(self):
        self.vibrate()

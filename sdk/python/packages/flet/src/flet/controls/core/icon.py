from typing import Optional

from flet.controls.base_control import control
from flet.controls.box import ShadowValue
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.types import BlendMode, IconValue, OptionalColorValue, OptionalNumber

__all__ = ["Icon"]


@control("Icon")
class Icon(ConstrainedControl):
    """
    Displays a Material icon.

    Icon browser: https://flet-icons-browser.fly.dev/#/

    Online docs: https://flet.dev/docs/controls/icon
    """

    name: IconValue
    """
    The name of the icon.

    You can search through the list of all available icons using open-source
    [Icons browser](https://gallery.flet.dev/icons-browser/) app
    [written in Flet](https://github.com/flet-dev/examples/blob/main/python/apps/icons-browser/main.py).
    """

    color: OptionalColorValue = None
    """
    Icon [color](https://flet.dev/docs/reference/colors).
    """

    size: OptionalNumber = None
    """
    The icon's size.

    Defaults to `24`.
    """

    semantics_label: Optional[str] = None
    """
    The semantics label for this icon.

    It is not shown to the in the UI, but is announced in accessibility modes
    (e.g. TalkBack/VoiceOver).
    """

    shadows: Optional[ShadowValue] = None
    """
    TBD
    """

    fill: OptionalNumber = None
    """
    TBD
    """

    apply_text_scaling: Optional[bool] = None
    """
    TBD
    """

    grade: OptionalNumber = None
    """
    TBD
    """

    weight: OptionalNumber = None
    """
    TBD
    """

    optical_size: OptionalNumber = None
    """
    TBD
    """

    blend_mode: Optional[BlendMode] = None
    """
    TBD
    """

    def before_update(self):
        super().before_update()
        assert self.fill is None or (
            0.0 <= self.fill <= 1.0
        ), "fill must be between 0.0 and 1.0 inclusive"
        assert self.weight is None or (
            self.weight > 0.0
        ), "weight must be strictly greater than 0.0"
        assert self.optical_size is None or (
            self.optical_size > 0.0
        ), "optical_size must be strictly greater than 0.0"

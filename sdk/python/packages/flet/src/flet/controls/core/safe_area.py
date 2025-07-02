from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.padding import PaddingValue

__all__ = ["SafeArea"]


@control("SafeArea")
class SafeArea(ConstrainedControl, AdaptiveControl):
    """
    A control that insets its `content` by sufficient padding to avoid intrusions by
    the operating system.

    For example, this will indent the `content` by enough to avoid the status bar at
    the top of the screen.

    It will also indent the `content` by the amount necessary to avoid The Notch on the
    iPhone X, or other similar creative physical features of the display.

    When a `minimum_padding` is specified, the greater of the minimum padding or the
    safe area padding will be applied.
    """

    content: Control
    """
    A `Control` to display inside safe area.
    """

    avoid_intrusions_left: bool = True
    """
    Whether to avoid system intrusions on the left.
    """

    avoid_intrusions_top: bool = True
    """
    Whether to avoid system intrusions at the top of the screen, typically the system
    status bar.
    """

    avoid_intrusions_right: bool = True
    """
    Whether to avoid system intrusions on the right.
    """

    avoid_intrusions_bottom: bool = True
    """
    Whether to avoid system intrusions on the bottom side of the screen.
    """

    maintain_bottom_view_padding: bool = False
    """
    Specifies whether the `SafeArea` should maintain the bottom
    `MediaQueryData.viewPadding` instead of the bottom `MediaQueryData.padding`.

    This avoids layout shifts caused by keyboard overlays, useful when flexible
    controls are used.
    """

    minimum_padding: PaddingValue = 0
    """
    This minimum padding to apply.

    The greater of the minimum insets and the media padding will be applied.
    """

    def before_update(self):
        super().before_update()
        assert self.content.visible, "content must be visible"

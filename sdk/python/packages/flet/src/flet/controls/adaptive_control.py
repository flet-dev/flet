from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control

__all__ = ["AdaptiveControl"]


@control(kw_only=True)
class AdaptiveControl(Control):
    """
    Base class for controls that support adaptive behavior, which allows them to adjust
    their appearance and behavior based on the target platform
    (ex: Material design on Android/Windows/Linux, Cupertino design on iOS/macOS).

    The [`adaptive`][(c).] property is applicable in two common scenarios:

    1. **Platform-adaptive controls**:
        These controls have a corresponding version on both Material and Cupertino
        platforms. When `adaptive` is set to `True`, the control renders the
        appropriate platform-specific implementation.

    2. **Container controls**:
        Controls that contain children (ex: [`Row`][flet.], [`Column`][flet.]) can pass
        the `adaptive` value down to their children that do not explicitly define it
        themselves. This enables nested adaptive behavior in complex layouts.

    Extension developers can use this base class to create their own adaptive controls
    by checking the `adaptive` flag at runtime and rendering accordingly.

    Note:
        This class does not implement any platform-specific rendering itself.
        It is up to the control inheriting from it to interpret the [`adaptive`][(c).]
        flag and render accordingly.
    """

    adaptive: Optional[bool] = None
    """
    Enables platform-specific rendering or inheritance of adaptiveness
    from parent controls.
    """

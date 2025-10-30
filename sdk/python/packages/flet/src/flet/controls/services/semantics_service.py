from dataclasses import dataclass
from enum import Enum

from flet.controls.base_control import control
from flet.controls.services.service import Service
from flet.utils import from_dict

__all__ = ["AccessibilityFeatures", "Assertiveness", "SemanticsService"]


class Assertiveness(Enum):
    """
    Determines the assertiveness level of the accessibility announcement.
    """

    POLITE = "polite"
    """
    The assistive technology will speak changes whenever the user is idle.
    """

    ASSERTIVE = "assertive"
    """
    The assistive technology will interrupt any announcement that it is
    currently making to notify the user about the change.

    It should only be used for time-sensitive/critical notifications.
    """


@dataclass
class AccessibilityFeatures:
    """
    Accessibility features that may be enabled by the platform.

    Note:
        It is not possible to enable these settings from Flet, instead they are
        used by the platform to indicate that additional accessibility features are
        enabled.
    """

    accessible_navigation: bool
    """
    Whether there is a running accessibility service which is changing the
    interaction model of the device.

    For example, TalkBack on Android and VoiceOver on iOS enable this flag.
    """

    bold_text: bool
    """
    The platform is requesting that text be rendered at a bold font weight.

    Note:
        Only supported on iOS and Android API 31+.
    """

    disable_animations: bool
    """
    The platform is requesting that animations be disabled or simplified.
    """

    high_contrast: bool
    """
    The platform is requesting that UI be rendered with darker colors.

    Note:
        Only supported on iOS.
    """

    invert_colors: bool
    """
    The platform is inverting the colors of the application.
    """

    reduce_motion: bool
    """
    The platform is requesting that certain animations be simplified and
    parallax effects removed.

    Note:
        Only supported on iOS.
    """

    on_off_switch_labels: bool
    """
    The platform is requesting to show on/off labels inside switches.

    Note:
        Only supported on iOS.
    """

    supports_announcements: bool
    """
    Whether the platform supports accessibility announcement API, i.e.
    [`SemanticsService.announce_message()`][flet.SemanticsService.announce_message].

    Will be `False` on platforms where announcements are deprecated or
    unsupported by the underlying platform and `True` on platforms where such
    announcements are generally supported without discouragement (ex: iOS, web).

    Note:
        Some platforms do not support or discourage the use of
        announcement. Using `SemanticsService.announce_message()` on those platforms
        may be ignored. Consider using other way to convey message to the
        user. For example, Android discourages the uses of direct message
        announcement, and rather encourages using other semantic
        properties such as [`Semantics.live_region`][flet.] to convey
        message to the user.
    """


@control("SemanticsService")
class SemanticsService(Service):
    """
    Allows access to the platform's accessibility services.
    """

    async def announce_tooltip(self, message: str):
        """
        Sends a semantic announcement of a tooltip.

        Note:
            Only supported on Android.
        """
        await self._invoke_method("announce_tooltip", arguments={"message": message})

    async def announce_message(
        self,
        message: str,
        rtl: bool = False,
        assertiveness: Assertiveness = Assertiveness.POLITE,
    ):
        """
        Sends a semantic announcement with the given message.

        Args:
            message: The message to be announced.
            rtl: Indicates if the message text direction is right-to-left.
            assertiveness: The assertiveness level of the announcement.
                Only supported on web.

        Notes:
            This method should be used for announcements that are not automatically
            handled by the system as a result of a UI state change.
        """
        await self._invoke_method(
            "announce_message",
            arguments={
                "message": message,
                "rtl": rtl,
                "assertiveness": assertiveness,
            },
        )

    async def get_accessibility_features(self) -> AccessibilityFeatures:
        """
        Returns the current platform accessibility feature flags.

        Returns:
            A snapshot of the platform's accessibility
                preferences at the time of invocation.
        """
        features = await self._invoke_method("get_accessibility_features")
        return from_dict(AccessibilityFeatures, features)

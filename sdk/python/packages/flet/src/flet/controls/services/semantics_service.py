from enum import Enum

from flet.controls.base_control import control
from flet.controls.services.service import Service

__all__ = ["Assertiveness", "SemanticsService"]


class Assertiveness(Enum):
    POLITE = "polite"
    ASSERTIVE = "assertive"


@control("SemanticsService")
class SemanticsService(Service):
    """
    Allows access to the platform's accessibility services.
    """

    async def announce_tooltip(self, message: str):
        """
        Sends a semantic announcement of a tooltip. Currently honored on Android only.

        The provided `message` will be read by TalkBack.
        """
        await self._invoke_method("announce_tooltip", arguments={"message": message})

    async def announce_message(
        self,
        message: str,
        rtl: bool = False,
        assertiveness: Assertiveness = Assertiveness.POLITE,
    ):
        """
        Sends a semantic announcement with the given `message`. This should preferably
        be used for announcements that are not seamlessly announced by the system as a
        result of a UI state change.

        `rtl` is a boolean and indicates the text direction of the `message`.

        The `assertiveness` level of the announcement is only supported by the web
        engine and has no effect on other platforms. Value is an `Assertiveness` enum
        and can either be `Assertiveness.ASSERTIVE` or `Assertiveness.POLITE` (default).
        """
        await self._invoke_method(
            "announce_message",
            arguments={
                "message": message,
                "rtl": rtl,
                "assertiveness": assertiveness,
            },
        )

import asyncio
from enum import Enum

from flet.controls.control import Service, control

__all__ = ["SemanticsService", "Assertiveness"]


class Assertiveness(Enum):
    POLITE = "polite"
    ASSERTIVE = "assertive"


@control("SemanticsService")
class SemanticsService(Service):
    async def announce_tooltip_async(self, message: str):
        await self._invoke_method_async(
            "announce_tooltip", arguments={"message": message}
        )

    def announce_tooltip(self, message: str):
        asyncio.create_task(self.announce_tooltip_async(message))

    async def announce_message_async(
        self,
        message: str,
        rtl: bool = False,
        assertiveness: Assertiveness = Assertiveness.POLITE,
    ):
        await self._invoke_method_async(
            "announce_message",
            arguments={
                "message": message,
                "rtl": str(rtl),
                "assertiveness": assertiveness,
            },
        )

    def announce_message(
        self,
        message: str,
        rtl: bool = False,
        assertiveness: Assertiveness = Assertiveness.POLITE,
    ):
        asyncio.create_task(self.announce_message_async(message, rtl, assertiveness))

from enum import Enum

from flet.controls.control import Service, control

__all__ = ["SemanticsService", "Assertiveness"]


class Assertiveness(Enum):
    POLITE = "polite"
    ASSERTIVE = "assertive"


@control("SemanticsService")
class SemanticsService(Service):
    def announce_message(
        self,
        message: str,
        rtl: bool = False,
        assertiveness: Assertiveness = Assertiveness.POLITE,
    ):
        self.invoke_method(
            "announce_message",
            arguments={
                "message": message,
                "rtl": str(rtl),
                "assertiveness": (
                    assertiveness.value
                    if isinstance(assertiveness, Assertiveness)
                    else str(assertiveness)
                ),
            },
        )

    def announce_tooltip(self, message: str):
        self.invoke_method(
            "announce_tooltip",
            arguments={
                "message": message,
            },
        )

from enum import Enum
from typing import Any, Optional

from flet_core.control import Control
from flet_core.ref import Ref


class Assertiveness(Enum):
    POLITE = "polite"
    ASSERTIVE = "assertive"


class SemanticsService(Control):
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
        return "semanticsservice"

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
                "assertiveness": assertiveness.value
                if isinstance(assertiveness, Assertiveness)
                else str(assertiveness),
            },
        )

    def announce_tooltip(self, message: str):
        self.invoke_method(
            "announce_tooltip",
            arguments={
                "message": message,
            },
        )

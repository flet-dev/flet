import time
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
        m = {
            "n": "announce",
            "i": str(time.time()),
            "p": {
                "message": message,
                "rtl": rtl,
                "assertiveness": assertiveness.value
                if isinstance(assertiveness, Assertiveness)
                else assertiveness,
            },
        }
        self._set_attr_json("method", m)

    def announce_tooltip(self, message: str):
        m = {
            "n": "tooltip",
            "i": str(time.time()),
            "p": {"message": message},
        }
        self._set_attr_json("method", m)

import dataclasses
import time
from typing import Optional

from beartype import beartype

from flet.control import Control
from flet.ref import Ref


@dataclasses.dataclass
class ClipboardData:
    ts: str
    d: Optional[str]


class Clipboard(Control):
    def __init__(
        self,
        ref: Ref = None,
        data: any = None,
        #
        # Specific
        #
        value: str = None,
    ):

        Control.__init__(
            self,
            ref=ref,
            data=data,
        )

        self.value = value

    def _get_control_name(self):
        return "clipboard"

    def _is_isolated(self):
        return True

    # value
    @property
    def value(self):
        return self.__value

    @value.setter
    @beartype
    def value(self, value: Optional[str]):
        self.__value = value
        cd = ClipboardData(str(time.time()), value)
        self._set_attr_json("value", cd)

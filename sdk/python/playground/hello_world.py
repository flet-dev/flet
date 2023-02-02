from typing import Optional

from flet_core.control import Control
from flet_core.ref import Ref


class HelloWorld(Control):

    def __init__(
        self,
        ref: Optional[Ref] = None,
    ):
        Control.__init__(self, ref=ref)

    def _get_control_name(self):
        return "helloworld"

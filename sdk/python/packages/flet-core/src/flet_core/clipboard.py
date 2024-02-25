import dataclasses
from typing import Any, Optional
from warnings import warn

from flet_core.control import Control
from flet_core.ref import Ref


@dataclasses.dataclass
class ClipboardData:
    ts: str
    d: Optional[str]


class Clipboard(Control):
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
        return "clipboard"

    def is_isolated(self):
        return True

    def set_data(self, data: str):
        self.invoke_method("set_data", {"data": data})

    async def set_data_async(self, data: str):
        warn("Obsolete. Use set_data() method instead.")
        self.set_data(data)

    def get_data(self) -> str:
        return self.invoke_method("get_data", wait_for_result=True)

    async def get_data_async(self) -> str:
        return await self.invoke_method_async("get_data", wait_for_result=True)

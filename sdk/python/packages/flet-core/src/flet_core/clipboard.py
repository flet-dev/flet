import dataclasses
import time
from typing import Any, Optional

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

    def _is_isolated(self):
        return True

    def set_data(self, data: str):
        self.page.invoke_method("set_data", {"data": data}, control_id=self.uid)

    async def set_data_async(self, data: str):
        await self.page.invoke_method_async(
            "set_data", {"data": data}, control_id=self.uid
        )

    def get_data(self) -> str:
        return self.page.invoke_method(
            "get_data", control_id=self.uid, wait_for_result=True
        )

    async def get_data_async(self) -> str:
        return await self.page.invoke_method_async(
            "get_data", control_id=self.uid, wait_for_result=True
        )

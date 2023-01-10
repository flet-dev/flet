import dataclasses
import time
from typing import Any, Optional

from flet_core.callable_control import CallableControl
from flet_core.ref import Ref


@dataclasses.dataclass
class ClipboardData:
    ts: str
    d: Optional[str]


class Clipboard(CallableControl):
    def __init__(
        self,
        ref: Optional[Ref] = None,
        data: Any = None,
    ):

        CallableControl.__init__(
            self,
            ref=ref,
            data=data,
        )

    def _get_control_name(self):
        return "clipboard"

    def _is_isolated(self):
        return True

    def set_data(self, data: str):
        self._call_method("set_data", [data], wait_for_result=False)

    async def set_data_async(self, data: str):
        await self._call_method_async("set_data", [data], wait_for_result=False)

    def get_data(self) -> str:
        return self._call_method("get_data", [])

    async def get_data_async(self) -> str:
        return await self._call_method_async("get_data", [])

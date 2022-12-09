import dataclasses
import json
import threading
from typing import Any, Dict, List, Optional

from flet.control import Control
from flet.ref import Ref


@dataclasses.dataclass
class ControlMethodCall:
    i: int
    n: str
    p: List[str]


@dataclasses.dataclass
class ControlMethodResults:
    i: int
    r: Optional[str]
    e: Optional[str]


class CallableControl(Control):
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

        self.__call_counter = 0
        self.__calls: Dict[int, threading.Event] = {}
        self.__results: Dict[threading.Event, tuple[Optional[str], Optional[str]]] = {}
        self._add_event_handler("method_result", self._on_result)

    def _call_method(self, name: str, params: List[str], wait_for_result=True) -> Any:
        m = ControlMethodCall(i=self.__call_counter, n=name, p=params)
        self.__call_counter += 1
        self._set_attr_json("method", m)

        evt: Optional[threading.Event] = None
        if wait_for_result:
            evt = threading.Event()
            self.__calls[m.i] = evt
        self.update()

        if not wait_for_result:
            return

        assert evt is not None
        if not evt.wait(5):
            del self.__calls[m.i]
            raise Exception(
                f"Timeout waiting for {self.__class__.__name__}.{name}({params}) method call"
            )
        result, err = self.__results.pop(evt)
        if err is not None:
            raise Exception(err)
        if result is None:
            return None
        return json.loads(result)

    def _on_result(self, e):
        d = json.loads(e.data)
        result = ControlMethodResults(**d)
        evt = self.__calls.pop(result.i, None)
        if evt is None:
            return
        self.__results[evt] = (result.r, result.e)
        evt.set()

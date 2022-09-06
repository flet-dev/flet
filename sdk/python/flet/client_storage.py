import dataclasses
import json
import threading
from multiprocessing import Event
from typing import Any, Dict, List, Optional
from unittest.main import main

from beartype import beartype

from flet.control import Control
from flet.ref import Ref


@dataclasses.dataclass
class ClientStorageMethodCall:
    i: int
    n: str
    p: List[str]


@dataclasses.dataclass
class ClientStorageMethodResults:
    i: int
    r: Optional[str]
    e: Optional[str]


class ClientStorage(Control):
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
        self._add_event_handler("result", self._on_result)

    def _get_control_name(self):
        return "clientstorage"

    def _is_isolated(self):
        return True

    def set(self, key: str, value: str):
        self._call_method("set", [key, value])

    def get(self, key: str):
        return self._call_method("get", [key])

    def _call_method(self, name: str, params: List[str]) -> Any:
        m = ClientStorageMethodCall(i=self.__call_counter, n=name, p=params)
        self.__call_counter += 1
        self._set_attr_json("method", m)
        evt = threading.Event()
        self.__calls[m.i] = evt
        self.update()
        if not evt.wait(5):
            del self.__calls[m.i]
            raise Exception(
                f"Timeout waiting for ClientStorage.{name}({params}) method call"
            )
        result, err = self.__results.pop(evt)
        if err != None:
            raise Exception(err)
        if result == None:
            return None
        return json.loads(result)

    def _on_result(self, e):
        d = json.loads(e.data)
        result = ClientStorageMethodResults(**d)
        evt = self.__calls.pop(result.i, None)
        if evt == None:
            return
        self.__results[evt] = (result.r, result.e)
        evt.set()

import asyncio
from typing import Callable

from flet_core.control_event import ControlEvent
from flet_core.types import OptionalEventCallable


class EventHandler:
    def __init__(self, result_converter=None) -> None:
        self.__result_converter = result_converter
        self.__handlers = {}

    def get_handler(self):
        async def fn(e: ControlEvent):
            for handler in self.__handlers.keys():
                ce = e
                if self.__result_converter is not None:
                    ce = self.__result_converter(e)
                    if ce is not None:
                        ce.target = e.target
                        ce.name = e.name
                        ce.data = e.data
                        ce.control = e.control
                        ce.page = e.page

                if ce is not None:
                    if asyncio.iscoroutinefunction(handler):
                        await handler(ce)
                    else:
                        e.page.run_thread(handler, ce)

        return fn

    def subscribe(self, handler: OptionalEventCallable):
        if handler is not None:
            self.__handlers[handler] = True

    def unsubscribe(self, handler: Callable[[ControlEvent], None]):
        if handler in self.__handlers:
            self.__handlers.pop(handler)

    def count(self) -> int:
        return len(self.__handlers)

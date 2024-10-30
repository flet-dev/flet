import asyncio

from flet.core.control_event import ControlEvent
from flet.core.types import OptionalControlEventCallable


class EventHandler:
    def __init__(self, result_converter=None) -> None:
        self.__result_converter = result_converter
        self.handler: OptionalControlEventCallable = None

    def get_handler(self):
        async def fn(e: ControlEvent):
            if self.handler is not None:
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
                    if asyncio.iscoroutinefunction(self.handler):
                        await self.handler(ce)
                    else:
                        e.page.run_thread(self.handler, ce)

        return fn

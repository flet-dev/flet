from typing import Optional

from flet.controls.base_control import control
from flet.controls.duration import Duration
from flet.controls.keys import KeyValue
from flet.controls.services.service import Service
from flet.controls.types import IconValue
from flet.testing.finder import Finder

__all__ = ["Tester"]


@control("Tester")
class Tester(Service):
    async def pump(self, duration: Optional[Duration] = None):
        return await self._invoke_method_async("pump", {"duration": duration})

    async def pump_and_settle(self):
        return await self._invoke_method_async("pump_and_settle")

    async def find_by_text(self, text: str):
        finder = await self._invoke_method_async("find_by_text", {"text": text})
        return Finder(**finder)

    async def find_by_text_containing(self, text: str):
        finder = await self._invoke_method_async(
            "find_by_text_containing", {"text": text}
        )
        return Finder(**finder)

    async def find_by_key(self, key: KeyValue):
        finder = await self._invoke_method_async("find_by_key", {"key": key})
        return Finder(**finder)

    async def find_by_tooltip(self, value: str):
        finder = await self._invoke_method_async("find_by_tooltip", {"value": value})
        return Finder(**finder)

    async def find_by_icon(self, icon: IconValue):
        finder = await self._invoke_method_async("find_by_icon", {"icon": icon})
        return Finder(**finder)

    async def tap(self, finder: Finder):
        await self._invoke_method_async("tap", {"id": finder.id})

    async def enter_text(self, finder: Finder, text: str):
        await self._invoke_method_async("enter_text", {"id": finder.id, "text": text})

    def teardown(self):
        return self._invoke_method_async("teardown")

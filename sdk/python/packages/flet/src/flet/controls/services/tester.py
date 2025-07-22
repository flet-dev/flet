from flet.controls.base_control import control
from flet.controls.services.service import Service

__all__ = ["Tester"]


@control("Tester")
class Tester(Service):
    async def pump_and_settle(self):
        return await self._invoke_method_async("pump_and_settle")

    async def count_by_text(self, text: str):
        return await self._invoke_method_async("count_by_text", {"text": text})

    def teardown(self):
        return self._invoke_method_async("teardown")

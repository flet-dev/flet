from typing import Optional

from flet.core.control import Service, control


@control("Clipboard")
class Clipboard(Service):

    def set(self, value: str, timeout: Optional[float] = 10) -> None:
        self.invoke_method("set", {"data": value}, timeout=timeout)

    def get(self, timeout: Optional[float] = 10) -> Optional[str]:
        return self.invoke_method("get", timeout=timeout)

    async def get_async(self, timeout: Optional[float] = 10) -> Optional[str]:
        return await self.invoke_method_async("get", timeout=timeout)

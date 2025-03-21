from typing import Optional

from flet.core.control import Service, control


@control("BrowserContextMenu")
class BrowserContextMenu(Service):

    def __post_init__(self, ref):
        Service.__post_init__(self, ref)
        self.__disabled = False

    def enable(self, wait_timeout: Optional[float] = 10):
        self.invoke_method("enable_menu", timeout=wait_timeout)
        self.__disabled = False

    def disable(self, wait_timeout: Optional[float] = 10):
        self.invoke_method("disable_menu", timeout=wait_timeout)
        self.__disabled = True

    @property
    def disabled(self):
        return self.__disabled

from typing import Optional

from flet.core.event import Event


class ControlEvent(Event):
    def __init__(self, target: str, name: str, data: Optional[str], control, page):
        Event.__init__(self, target=target, name=name, data=data)

        self.control = control
        self.page = page

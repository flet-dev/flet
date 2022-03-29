from flet.event import Event


class ControlEvent(Event):
    def __init__(self, target, name, data, control, page):
        Event.__init__(self, target=target, name=name, data=data)

        self.control = control
        self.page = page

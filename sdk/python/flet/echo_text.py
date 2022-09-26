"""Echo text control demo."""


import flet
from flet.constrained_control import ConstrainedControl


class EchoText(ConstrainedControl):
    def __init__(self, message: str = None, **kwds):
        super().__init__(**kwds)
        self._add_event_handler("click", self.on_click)
        self.message = message
        return

    def _get_control_name(self):
        return "echotext"

    def _get_children(self):
        return []

    @property
    def echoed(self):
        """Access the Text widget containing echoed text."""
        return self._get_attr("echoed")

    @echoed.setter
    def echoed(self, value: str):
        return self._set_attr("echoed", value)

    @property
    def message(self):
        """Access the TextField widget where text is entered."""
        return self._get_attr("message")

    @message.setter
    def message(self, value: str):
        return self._set_attr("message", value)

    # def on_change(self, e: flet.Event):
    #     self.message = e.data
    #     return

    def on_click(self, e: flet.Event):
        """Handle button click that updates the `echoed`.

        This gets whatever is currently typed, changes and sends it back.
        """
        self.echoed = f'I got "{self.message}"...'
        self.update()
        return

from flet.control import Control
from flet.ref import Ref


class Clipboard(Control):
    def __init__(
        self,
        ref: Ref = None,
        data: any = None,
        #
        # Specific
        #
        value: str = None,
    ):

        Control.__init__(
            self,
            ref=ref,
            data=data,
        )

        self.value = value

    def _get_control_name(self):
        return "clipboard"

    # value
    @property
    def value(self):
        return self._get_attr("value")

    @value.setter
    def value(self, value):
        self._set_attr("value", value)

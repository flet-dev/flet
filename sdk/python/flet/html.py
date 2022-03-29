from flet.control import Control


class Html(Control):
    def __init__(self, value=None, id=None, ref=None, visible=None):

        Control.__init__(self, id=id, ref=ref, visible=visible)

        self.value = value

    def _get_control_name(self):
        return "html"

    # value
    @property
    def value(self):
        return self._get_attr("value")

    @value.setter
    def value(self, value):
        self._set_attr("value", value)

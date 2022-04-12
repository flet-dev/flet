from typing import Optional

from beartype import beartype

from flet.control import Control
from flet.ref import Ref

try:
    from typing import Literal
except:
    from typing_extensions import Literal


class SnackBar(Control):
    def __init__(
        self,
        id: str = None,
        ref: Ref = None,
        disabled: bool = None,
        data: any = None,
        #
        # Specific
        #
        open: bool = False,
        content: str = None,
    ):

        Control.__init__(
            self,
            id=id,
            ref=ref,
            disabled=disabled,
            data=data,
        )

        self.open = open
        self.content = content

    def _get_control_name(self):
        return "snackbar"

    # content
    @property
    def content(self):
        return self._get_attr("content")

    @content.setter
    def content(self, value):
        self._set_attr("content", value)

    # open
    @property
    def open(self):
        return self._get_attr("open", data_type="bool", def_value=False)

    @open.setter
    @beartype
    def open(self, value: Optional[bool]):
        self._set_attr("open", value)

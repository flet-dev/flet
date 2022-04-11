from typing import Optional

from beartype import beartype

from flet.control import Control
from flet.ref import Ref

try:
    from typing import Literal
except:
    from typing_extensions import Literal


ImageFit = Literal[
    None, "none", "contain", "cover", "fill", "fitHeight", "fitWidth", "scaleDown"
]

ImageRepeat = Literal[None, "noRepeat", "repeat", "repeatX", "repeatY"]


class Image(Control):
    def __init__(
        self,
        id: str = None,
        ref: Ref = None,
        width: float = None,
        height: float = None,
        padding: float = None,
        margin: float = None,
        expand: int = None,
        opacity: float = None,
        visible: bool = None,
        disabled: bool = None,
        data: any = None,
        #
        # Specific
        #
        src=None,
        repeat: ImageRepeat = None,
        fit: ImageFit = None,
    ):

        Control.__init__(
            self,
            id=id,
            ref=ref,
            width=width,
            height=height,
            padding=padding,
            margin=margin,
            expand=expand,
            opacity=opacity,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.src = src
        self.fit = fit
        self.repeat = repeat

    def _get_control_name(self):
        return "image"

    # src
    @property
    def src(self):
        return self._get_attr("src")

    @src.setter
    def src(self, value):
        self._set_attr("src", value)

    # fit
    @property
    def fit(self):
        return self._get_attr("fit")

    @fit.setter
    @beartype
    def fit(self, value: ImageFit):
        self._set_attr("fit", value)

    # repeat
    @property
    def repeat(self):
        return self._get_attr("repeat")

    @repeat.setter
    @beartype
    def repeat(self, value: ImageRepeat):
        self._set_attr("repeat", value)

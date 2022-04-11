from typing import Optional

from beartype import beartype

from flet.control import Control

try:
    from typing import Literal
except:
    from typing_extensions import Literal


Fit = Literal[
    None, "none", "contain", "cover", "center", "centerContain", "centerCover"
]


class Image(Control):
    def __init__(
        self,
        src=None,
        id=None,
        ref=None,
        alt=None,
        title=None,
        maximize_frame=None,
        fit: Fit = None,
        width=None,
        height=None,
        padding=None,
        margin=None,
        visible=None,
        disabled=None,
    ):

        Control.__init__(
            self,
            id=id,
            ref=ref,
            width=width,
            height=height,
            padding=padding,
            margin=margin,
            visible=visible,
            disabled=disabled,
        )

        self.src = src
        self.alt = alt
        self.title = title
        self.fit = fit
        self.maximize_frame = maximize_frame

    def _get_control_name(self):
        return "image"

    # src
    @property
    def src(self):
        return self._get_attr("src")

    @src.setter
    def src(self, value):
        self._set_attr("src", value)

    # alt
    @property
    def alt(self):
        return self._get_attr("alt")

    @alt.setter
    def alt(self, value):
        self._set_attr("alt", value)

    # title
    @property
    def title(self):
        return self._get_attr("title")

    @title.setter
    def title(self, value):
        self._set_attr("title", value)

    # maximize_frame
    @property
    def maximize_frame(self):
        return self._get_attr("maximizeFrame", data_type="bool", def_value=False)

    @maximize_frame.setter
    @beartype
    def maximize_frame(self, value: Optional[bool]):
        self._set_attr("maximizeFrame", value)

    # fit
    @property
    def fit(self):
        return self._get_attr("fit")

    @fit.setter
    @beartype
    def fit(self, value: Fit):
        self._set_attr("fit", value)

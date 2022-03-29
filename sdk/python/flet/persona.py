from typing import Optional

from beartype import beartype

from flet.control import Control

try:
    from typing import Literal
except:
    from typing_extensions import Literal


Size = Literal[None, 8, 24, 32, 40, 48, 56, 72, 100, 120]

Presence = Literal[None, "none", "offline", "online", "away", "blocked", "busy", "dnd"]

InitialsColor = Literal[
    None,
    "blue",
    "burgundy",
    "coolGray",
    "cyan",
    "darkBlue",
    "darkGreen",
    "darkRed",
    "gold",
    "green",
    "lightBlue",
    "lightGreen",
    "lightPink",
    "lightRed",
    "magenta",
    "orange",
    "pink",
    "purple",
    "rust",
    "teal",
    "transparent",
    "violet",
    "warmGray",
]


class Persona(Control):
    def __init__(
        self,
        text=None,
        id=None,
        ref=None,
        image_url=None,
        image_alt=None,
        initials_color: InitialsColor = None,
        initials_text_color=None,
        secondary_text=None,
        tertiary_text=None,
        optional_text=None,
        size: Size = None,
        presence: Presence = None,
        hide_details=None,
        visible=None,
    ):

        Control.__init__(self, id=id, ref=ref, visible=visible)

        self.text = text
        self.image_url = image_url
        self.image_alt = image_alt
        self.initials_color = initials_color
        self.initials_text_color = initials_text_color
        self.secondary_text = secondary_text
        self.tertiary_text = tertiary_text
        self.optional_text = optional_text
        self.size = size
        self.presence = presence
        self.hide_details = hide_details

    def _get_control_name(self):
        return "persona"

    # text
    @property
    def text(self):
        return self._get_attr("text")

    @text.setter
    def text(self, value):
        self._set_attr("text", value)

    # image_url
    @property
    def image_url(self):
        return self._get_attr("imageurl")

    @image_url.setter
    def image_url(self, value):
        self._set_attr("imageurl", value)

    # image_alt
    @property
    def image_alt(self):
        return self._get_attr("imagealt")

    @image_alt.setter
    def image_alt(self, value):
        self._set_attr("imagealt", value)

    # initials_color
    @property
    def initials_color(self):
        return self._get_attr("initialscolor")

    @initials_color.setter
    @beartype
    def initials_color(self, value: InitialsColor):
        self._set_attr("initialscolor", value)

    # initials_text_color
    @property
    def initials_text_color(self):
        return self._get_attr("initialstextcolor")

    @initials_text_color.setter
    def initials_text_color(self, value):
        self._set_attr("initialstextcolor", value)

    # secondary_text
    @property
    def secondary_text(self):
        return self._get_attr("secondarytext")

    @secondary_text.setter
    def secondary_text(self, value):
        self._set_attr("secondarytext", value)

    # tertiary_text
    @property
    def tertiary_text(self):
        return self._get_attr("tertiarytext")

    @tertiary_text.setter
    def tertiary_text(self, value):
        self._set_attr("tertiarytext", value)

    # optional_text
    @property
    def optional_text(self):
        return self._get_attr("optionaltext")

    @optional_text.setter
    def optional_text(self, value):
        self._set_attr("optionaltext", value)

    # size
    @property
    def size(self):
        return self._get_attr("size")

    @size.setter
    @beartype
    def size(self, value: Size):
        self._set_attr("size", value)

    # presence
    @property
    def presence(self):
        return self._get_attr("presence")

    @presence.setter
    @beartype
    def presence(self, value: Presence):
        self._set_attr("presence", value)

    # hide_details
    @property
    def hide_details(self):
        return self._get_attr("hidedetails", data_type="bool", def_value=False)

    @hide_details.setter
    @beartype
    def hide_details(self, value: Optional[bool]):
        self._set_attr("hidedetails", value)

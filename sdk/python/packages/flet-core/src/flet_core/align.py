from typing import Optional
from flet_core.adaptive_control import AdaptiveControl
from flet_core.alignment import Alignment
from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref


class Align(ConstrainedControl, AdaptiveControl):
    """
    align allows to place a control into a specific position, with the alignment, height_factor and width_factor.

    Example:

    ```
    from flet import *

    def main(page:Page):
    page.title = "Align"

    page.add(
        Stack(
            controls=[
                Align(
                    content=Text(
                        "Atas | Top",
                        style=TextStyle(
                            size=24,
                            color=colors.GREEN_900,
                            weight=FontWeight.W_600,
                        ),
                    ),
                    alignment=alignment.top_center,
                ),
                Align(
                    content=Text(
                        "Bawah | Bottom",
                        style=TextStyle(
                            size=24,
                            color=colors.BLUE_900,
                            weight=FontWeight.W_600,
                        ),
                    ),
                    alignment=alignment.bottom_center,
                ),
                Align(
                    content=Text(
                        "Tengah | Center",
                        style=TextStyle(
                            size=24,
                            color=colors.RED_800,
                            weight=FontWeight.W_600,
                        ),
                    ),
                    alignment=alignment.center,
                ),
            ],
            height=page.height,
            width=page.width,
        ),
    )

    ```


    -----

    Online docs: https://flet.dev/docs/controls/align
    """

    def __init__(
        self,
        content: Optional[Control] = None,
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        #
        # Spesific
        #
        alignment: Optional[Alignment] = None,
        width_factor: OptionalNumber = None,
        height_factor: OptionalNumber = None,
        #
        # Adaptive
        #
        adaptive: Optional[bool] = None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            key=key,
        )

        AdaptiveControl.__init__(self, adaptive=adaptive)

        self.content = content
        self.alignment = alignment
        self.height_factor = height_factor
        self.width_factor = width_factor

    def _get_control_name(self):
        return "align"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("alignment", self.__alignment)
        self._set_attr_json("height_factor", self.__heightFactor)
        self._set_attr_json("width_factor", self.__widthFactor)

    def _get_children(self):
        children = []
        if self.__content is not None:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)

        return children

    # alignment
    @property
    def alignment(self) -> Optional[Alignment]:
        """:obj:`Alignment`, optional: Align the child control within the container.

        Alignment is an instance of `alignment.Alignment` class object with `x` and `y` properties
        representing the distance from the center of a rectangle.
        """
        return self.__alignment

    @alignment.setter
    def alignment(self, value: Optional[Alignment]):
        self.__alignment = value

    # height_factor
    @property
    def height_factor(self):
        return self.__heightFactor

    @height_factor.setter
    def height_factor(self, value: OptionalNumber):
        self.__heightFactor = value

    # width_factor
    @property
    def width_factor(self):
        return self.__widthFactor

    @width_factor.setter
    def width_factor(self, value: OptionalNumber):
        self.__widthFactor = value

    # content
    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value

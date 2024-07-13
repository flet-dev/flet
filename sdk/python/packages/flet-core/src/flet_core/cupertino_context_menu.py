from typing import Any, List, Optional

from flet_core.adaptive_control import AdaptiveControl
from flet_core.control import Control
from flet_core.ref import Ref


class CupertinoContextMenu(AdaptiveControl):
    """
    A full-screen modal route that opens up when the content is long-pressed.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinocontextmenu
    """

    def __init__(
        self,
        content: Control,
        actions: List[Control],
        enable_haptic_feedback: Optional[bool] = None,
        #
        # Control
        #
        ref: Optional[Ref] = None,
        disabled: Optional[bool] = None,
        visible: Optional[bool] = None,
        data: Any = None,
        adaptive: Optional[bool] = False,
    ):
        Control.__init__(
            self,
            ref=ref,
            disabled=disabled,
            visible=visible,
            data=data,
        )

        AdaptiveControl.__init__(self, adaptive=adaptive)

        self.enable_haptic_feedback = enable_haptic_feedback
        self.content = content
        self.actions = actions

    def _get_control_name(self):
        return "cupertinocontextmenu"

    def _get_children(self):
        self.__content._set_attr_internal("n", "content")
        for action in self.__actions:
            action._set_attr_internal("n", "action")
        return [self.__content] + self.__actions

    def before_update(self):
        super().before_update()
        assert (
            len(self.__actions) > 0
        ), "actions must be provided and at least one must be visible"

    # enable_haptic_feedback
    @property
    def enable_haptic_feedback(self) -> bool:
        return self._get_attr("enableHapticFeedback", data_type="bool", def_value=False)

    @enable_haptic_feedback.setter
    def enable_haptic_feedback(self, value: Optional[bool]):
        self._set_attr("enableHapticFeedback", value)

    # content
    @property
    def content(self) -> Control:
        return self.__content

    @content.setter
    def content(self, value: Control):
        self.__content = value

    # actions
    @property
    def actions(self) -> List[Control]:
        return self.__actions

    @actions.setter
    def actions(self, value: List[Control]):
        self.__actions = value

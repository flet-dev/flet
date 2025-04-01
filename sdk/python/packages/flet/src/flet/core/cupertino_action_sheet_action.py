from typing import Optional

from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, control
from flet.core.types import OptionalControlEventCallable


@control("CupertinoActionSheetAction")
class CupertinoActionSheetAction(ConstrainedControl):
    """
    An action button typically used in a CupertinoActionSheet.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinoactionsheetaction
    """

    text: Optional[str] = None
    content: Optional[Control] = None
    is_default_action: Optional[bool] = None
    is_destructive_action: Optional[bool] = None
    on_click: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert self.text is not None or (
            (self.content is not None and self.content.visible)
        ), "text or (visible) content must be provided visible"

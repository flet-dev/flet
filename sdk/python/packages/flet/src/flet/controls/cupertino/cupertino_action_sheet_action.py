from typing import Optional

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.types import MouseCursor, OptionalControlEventCallable, StrOrControl
from flet.utils import deprecated_warning

__all__ = ["CupertinoActionSheetAction"]


@control("CupertinoActionSheetAction")
class CupertinoActionSheetAction(ConstrainedControl):
    """
    An action button typically used in a CupertinoActionSheet.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinoactionsheetaction
    """

    def __setattr__(self, name, value):
        if name == "text" and value is not None:
            deprecated_warning(
                name="text",
                reason="Use content instead.",
                version="0.70.0",
                delete_version="0.73.0",
            )
        super().__setattr__(name, value)

    content: Optional[StrOrControl] = None  # todo(0.70.3): make required
    text: Optional[str] = None  # todo(0.70.3): remove in favor of content
    is_default_action: bool = False
    is_destructive_action: bool = False
    mouse_cursor: Optional[MouseCursor] = None
    on_click: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert (
            self.content is not None
            and (isinstance(self.content, str) or self.content.visible)
        ) or self.text is not None, "either text or a visible content must be provided"

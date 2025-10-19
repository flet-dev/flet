from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.layout_control import LayoutControl
from flet.controls.types import StrOrControl

__all__ = ["CupertinoActionSheet"]


@control("CupertinoActionSheet")
class CupertinoActionSheet(LayoutControl):
    """
    An iOS-style action sheet.

    Action sheets are generally used to give the user a choice between
    two or more choices for the current context.

    ```python
    sheet = ft.CupertinoActionSheet(
        title=ft.Text("Choose an option"),
        message=ft.Text("Select what you would like to do"),
        actions=[
            ft.CupertinoActionSheetAction(content=ft.Text("Save")),
            ft.CupertinoActionSheetAction(
                content=ft.Text("Delete"), destructive=True
            ),
        ],
        cancel=ft.CupertinoActionSheetAction(content=ft.Text("Cancel")),
    )
    page.show_dialog(ft.CupertinoBottomSheet(sheet))
    ```
    """

    title: Optional[StrOrControl] = None
    """
    A control containing the title of the action sheet.

    Typically a [`Text`][flet.] control.
    """

    message: Optional[StrOrControl] = None
    """
    A control containing a descriptive message that provides more details about the
    reason for the alert.

    Typically a [`Text`][flet.] control.
    """

    actions: Optional[list[Control]] = None
    """
    A list of action buttons to be shown in the sheet.

    These actions are typically [`CupertinoActionSheetAction`][flet.]s.

    Raises:
        ValueError: If none of [`actions`][(c).], [`title`][(c).], [`message`][(c).],
            or [`cancel`][(c).] are provided.
    """

    cancel: Optional[Control] = None
    """
    An optional control to be shown below the actions but grouped separately from them.

    Typically a [`CupertinoActionSheetAction`][flet.] button.
    """

    def before_update(self):
        super().before_update()
        if not (
            self.actions is not None
            or self.title is not None
            or self.message is not None
            or self.cancel is not None
        ):
            raise ValueError(
                "This action sheet must have a non-None value for at least one of the "
                "following arguments: `actions`, `title`, `message`, or `cancel`"
            )

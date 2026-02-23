from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.layout_control import LayoutControl
from flet.controls.types import StrOrControl
from flet.controls.validation import V, ValidationRules

__all__ = ["CupertinoActionSheet"]


@control("CupertinoActionSheet")
class CupertinoActionSheet(LayoutControl):
    """
    An iOS-style action sheet.

    Action sheets are generally used to give the user a choice between
    two or more choices for the current context.

    Example:
    ```python
    sheet = ft.CupertinoActionSheet(
        title=ft.Text("Choose an option"),
        message=ft.Text("Select what you would like to do"),
        cancel=ft.CupertinoActionSheetAction(content=ft.Text("Cancel")),
        actions=[
            ft.CupertinoActionSheetAction(content=ft.Text("Save")),
            ft.CupertinoActionSheetAction(
                content=ft.Text("Delete"), destructive=True
            ),
        ],
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
    A control containing a descriptive message that provides more details about the \
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
    An optional control to be shown below the actions but grouped separately from \
    them.

    Typically a [`CupertinoActionSheetAction`][flet.] button.
    """

    __validation_rules__: ValidationRules = (
        V.ensure(
            lambda ctrl: (
                (
                    isinstance(ctrl.actions, list)
                    and any(action.visible for action in ctrl.actions)
                )
                or (
                    isinstance(ctrl.title, str)
                    or (isinstance(ctrl.title, Control) and ctrl.title.visible)
                )
                or (
                    isinstance(ctrl.message, str)
                    or (isinstance(ctrl.message, Control) and ctrl.message.visible)
                )
                or (ctrl.cancel is not None and ctrl.cancel.visible)
            ),
            message=(
                "This action sheet must have a non-None value for at least one of the "
                "following arguments: `actions`, `title`, `message`, or `cancel`"
            ),
        ),
    )

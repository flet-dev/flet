from flet.controls.base_control import control
from flet.controls.material.elevated_button import ElevatedButton


@control("FilledButton")
class FilledButton(ElevatedButton):
    """
    Filled buttons have the most visual impact after the FloatingActionButton (https://flet.dev/docs/controls/floatingactionbutton),
    and should be used for important, final actions that complete a flow, like Save,
    Join now, or Confirm.

    Online docs: https://flet.dev/docs/controls/filledbutton
    """

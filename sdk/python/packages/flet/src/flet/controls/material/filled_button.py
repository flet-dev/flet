from flet.controls.base_control import control
from flet.controls.material.elevated_button import ElevatedButton


@control("FilledButton")
class FilledButton(ElevatedButton):
    """
    Filled buttons have the most visual impact after the [`FloatingActionButton`][flet.FloatingActionButton],
    and is typically used for important, final actions that complete a flow, like "Save",
    "Join now", or "Confirm".
    """

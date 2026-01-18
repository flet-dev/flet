from flet.controls.material.button import Button
from flet.utils.deprecated import deprecated_class

__all__ = ["ElevatedButton"]


@deprecated_class(
    reason="Use Button instead.",
    version="0.80.0",
    delete_version="1.0",
)
class ElevatedButton(Button):
    pass

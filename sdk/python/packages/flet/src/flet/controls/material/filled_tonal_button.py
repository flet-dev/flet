from flet.controls.base_control import control
from flet.controls.material.button import Button


@control("FilledTonalButton")
class FilledTonalButton(Button):
    """
    A filled tonal button is an alternative middle ground between FilledButton and
    OutlinedButton buttons. They're useful in contexts where a lower-priority button
    requires slightly more emphasis than an outline would give, such as "Next" in an
    onboarding flow. Tonal buttons use the secondary color mapping.

    ```python
    ft.FilledTonalButton(content="Tap me")
    ```
    """

    pass

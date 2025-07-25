from flet.controls.base_control import control
from flet.controls.material.elevated_button import ElevatedButton


@control("FilledTonalButton")
class FilledTonalButton(ElevatedButton):
    """
    A filled tonal button is an alternative middle ground between FilledButton and
    OutlinedButton buttons. They’re useful in contexts where a lower-priority button
    requires slightly more emphasis than an outline would give, such as "Next" in an
    onboarding flow. Tonal buttons use the secondary color mapping.
    """

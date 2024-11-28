from flet.core.elevated_button import ElevatedButton


class FilledTonalButton(ElevatedButton):
    """
    A filled tonal button is an alternative middle ground between FilledButton and OutlinedButton buttons. They’re useful in contexts where a lower-priority button requires slightly more emphasis than an outline would give, such as "Next" in an onboarding flow. Tonal buttons use the secondary color mapping.

    Example:
    ```
    import flet as ft


    def main(page: ft.Page):
        page.title = "Basic filled tonal buttons"
        page.add(
            ft.FilledTonalButton(text="Filled tonal button"),
            ft.FilledTonalButton("Disabled button", disabled=True),
            ft.FilledTonalButton("Button with icon", icon="add"),
        )

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/filledtonalbutton
    """

    def _get_control_name(self):
        return "filledtonalbutton"

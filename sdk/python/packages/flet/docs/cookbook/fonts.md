## System fonts

You can use the (system) fonts installed on your computer, e.g. "Consolas", "Arial", "Verdana", "Tahoma", etc.

/// admonition | Limitation
    type: note
System fonts cannot be used in Flet web apps rendered with [canvas kit][flet.WebRenderer.CANVAS_KIT] web renderer.
///

### Usage Example

The following example demonstrates how to use the "Consolas" font in a Flet application.

```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.Text(
            value="This text is rendered with Consolas font",
            font_family="Consolas"
        )
    )

ft.run(main)
```
## Importing Fonts
Font can be imported from external resource by providing an absolute URL or 
from application assets directory (see [Assets Guide](assets.md)).

This is done by setting the page's [`fonts`][flet.Page.fonts] property.

To apply one of the imported fonts, you can:
- Use [`Theme.font_family`][flet.Theme.font_family] to set a default/fallback app-wide font family.
- Specify a font for individual controls. For example, [`Text.font_family`][flet.Text.font_family].

### Usage Example
The example below loads the "Kanit" font from GitHub and "Open Sans" from local assets. "Kanit" is set as the default app font, while "Open Sans" is applied to a specific `Text` control.

```python
import flet as ft

def main(page: ft.Page):
    page.fonts = {
        "Kanit": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf",
        "Open Sans": "/fonts/OpenSans-Regular.ttf"
    }

    page.theme = Theme(font_family="Kanit")  # Default app font

    page.add(
        ft.Text("This text uses the Kanit font"),
        ft.Text("This text uses the Open Sans font", font_family="Open Sans")
    )

ft.run(main, assets_dir="assets")
```

### Static and Variable Fonts
Currently, only [static fonts](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Fonts/Variable_Fonts_Guide#standard_or_static_fonts) are supported. These fonts have a specific width, weight, or style combination (e.g., "Open Sans Regular").

Support for [variable fonts](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Fonts/Variable_Fonts_Guide#variable_fonts) is in progress. 

However, to use variable fonts, you can create static instances at specific weights using [fonttools](https://pypi.org/project/fonttools/), e.g.:

    ```bash
    fonttools varLib.mutator ./YourVariableFont-VF.ttf wght=140 wdth=85
    ```

To explore available font features (e.g. possible options for `wght`) use [Wakamai Fondue](https://wakamaifondue.com/beta/) online tool.


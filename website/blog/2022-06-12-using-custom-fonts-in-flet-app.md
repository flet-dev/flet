---
slug: using-custom-fonts-in-flet-app
title: Using custom fonts in a Flet app
authors: feodor
tags: [how-to]
---

You can now use your own fonts in a Flet app!

The following font formats are supported:

* `.ttc`
* `.ttf`
* `.otf`

Use [`page.fonts`](https://docs.flet.dev/controls/page/#flet.Page.fonts) property to import fonts.

<!-- truncate -->

Set `page.fonts` property to a dictionary where key is the font family name to refer that font and the value is the URL of the font file to import:

```python
def main(page: ft.Page):
    page.fonts = {
        "Kanit": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf",
        "Aleo Bold Italic": "https://raw.githubusercontent.com/google/fonts/master/ofl/aleo/Aleo-BoldItalic.ttf"
    }
    page.update()

    # ...
```

Font can be imported from external resource by providing an absolute URL or from application assets by providing relative URL and `assets_dir`.

Specify `assets_dir` in `flet.app()` call to set the location of assets that should be available to the application. `assets_dir` could be a relative to your `main.py` directory or an absolute path. For example, consider the following program structure:

```
/assets
   /fonts
       /OpenSans-Regular.ttf
main.py
```

## Code sample

The following program loads "Kanit" font from GitHub and "Open Sans" from the assets. "Kanit" is set as a default app font and "Open Sans" is used for a specific Text control:

```python
import flet as ft

def main(page: ft.Page):
    page.title = "Custom fonts"

    page.fonts = {
        "Kanit": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf",
        "Open Sans": "fonts/OpenSans-Regular.ttf",
    }

    page.theme = ft.Theme(font_family="Kanit")

    page.add(
        ft.Text("This is rendered with Kanit font"),
        ft.Text("This is Open Sans font example", font_family="Open Sans"),
    )

ft.run(main, assets_dir="assets")
```

<img src="/img/blog/using-custom-fonts-in-flet-app/custom-fonts-example.png" className="screenshot-50" />

## Static vs Variable fonts

At the moment only [static](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Fonts/Variable_Fonts_Guide#standard_or_static_fonts) fonts are supported, i.e. fonts containing only one specific width/weight/style combination, for example "Open Sans Regular" or "Roboto Bold Italic".

[Variable](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Fonts/Variable_Fonts_Guide#variable_fonts) fonts support is still [work in progress](https://github.com/flutter/flutter/issues/33709).

However, if you need to use a variable font in your app you can create static "instantiations" at specific weights using [fonttools](https://pypi.org/project/fonttools/), then use those:

    fonttools varLib.mutator ./YourVariableFont-VF.ttf wght=140 wdth=85

To explore available font features (e.g. possible options for `wght`) use [Wakamai Fondue](https://wakamaifondue.com/beta/) online tool.

[Give Flet a try](https://docs.flet.dev/) and [let us know](https://discord.gg/dzWXP8SHG8) what you think!


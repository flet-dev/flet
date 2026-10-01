---
examples: "extensions/shadcn_ui"
title: "Shadcn"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';

# Shadcn

Controls styled after [Shadcn](https://ui.shadcn.com), built on the Flutter
[`shadcn_ui`](https://pub.dev/packages/shadcn_ui) package, plus the
[Lucide](https://lucide.dev) icon set.

## Usage

Add `flet-shadcn-ui` to your project dependencies:

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```bash
uv add flet-shadcn-ui
```

</TabItem>
<TabItem value="pip" label="pip">
```bash
pip install flet-shadcn-ui  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
</TabItem>
</Tabs>

Then import it, typically under the `shad` alias:

```python
import flet as ft
import flet_shadcn_ui as shad


def main(page: ft.Page):
    page.add(shad.Button("Continue", leading=shad.LucideIcons.ARROW_RIGHT))


ft.run(main)
```

## Theming

The controls work without any setup. A control that is not inside a
[`Theme`](theme.md) uses the [`SLATE`][flet_shadcn_ui.ColorScheme.SLATE] color
scheme and follows the page's light or dark [`theme_mode`][flet.BasePage.theme_mode].

To use another color scheme, a fixed brightness or a different corner radius,
wrap controls in a [`Theme`](theme.md):

```python
shad.Theme(
    color_scheme=shad.ColorScheme.VIOLET,
    content=ft.Column([shad.Button("Save"), shad.Switch(label="Notify me")]),
)
```

## Icons

[`LucideIcons`](types/lucideicons.md) contains the Lucide icons. It can be used
anywhere Flet accepts an icon, including core controls such as
[`Icon`][flet.Icon] and [`IconButton`][flet.IconButton].

## Available controls

- [Theme](theme.md)
- [Alert](alert.md)
- [Avatar](avatar.md)
- [Badge](badge.md)
- [Breadcrumb](breadcrumb.md)
- [Button](button.md)
- [Card](card.md)
- [Checkbox](checkbox.md)
- [IconButton](iconbutton.md)
- [Input](input.md)
- [InputOTP](inputotp.md)
- [Progress](progress.md)
- [RadioGroup](radiogroup.md)
- [Select](select.md)
- [Separator](separator.md)
- [Slider](slider.md)
- [Switch](switch.md)
- [Tabs](tabs.md)
- [Textarea](textarea.md)

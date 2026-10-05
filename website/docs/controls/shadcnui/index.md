---
examples: "extensions/shadcn_ui"
example_images: "test-images/examples/extensions/shadcn_ui/golden/macos/form"
title: "Shadcn"
---

import {CodeExample, Image} from '@site/src/components/crocodocs';
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

## Forms

Value controls can show a label, helper text and a validation error, so a form
is a column of fields validated in your Python code.

[Input](input.md), [Textarea](textarea.md), [Select](select.md),
[InputOTP](inputotp.md), [DatePicker](datepicker.md),
[DateRangePicker](daterangepicker.md), [TimePicker](timepicker.md) and
[RadioGroup](radiogroup.md) have these properties:

- `label` is shown above the field.
- `description` is helper text shown below the field.
- `error_text` is an error message shown in red below the field. While it is
  set, the label and the field's border turn red too.

[Checkbox](checkbox.md) and [Switch](switch.md) already have a `label` and a
`sublabel` next to them, so they only add `error_text`.

<Image src={frontMatter.example_images + '/image_for_docs.png'} alt="form fields" width="35%" caption="Label, description and error" />

To validate, check the values in an event handler and set `error_text` on each
invalid field. Set it back to `None` once the value is valid. This sign-up form
shows errors when it is submitted, and after that each field checks itself
again as it changes:

<CodeExample path={frontMatter.examples + '/form/main.py'} language="python" />

<Image src={frontMatter.example_images + '/form_flow.gif'} alt="form" width="40%" caption="Submitting and correcting the form" />

## Available controls

- [Theme](theme.md)
- [Accordion](accordion.md)
- [Alert](alert.md)
- [Avatar](avatar.md)
- [Badge](badge.md)
- [Breadcrumb](breadcrumb.md)
- [Button](button.md)
- [Calendar](calendar.md)
- [Card](card.md)
- [Checkbox](checkbox.md)
- [ContextMenu](contextmenu.md)
- [DatePicker](datepicker.md)
- [DateRangePicker](daterangepicker.md)
- [Dialog](dialog.md)
- [IconButton](iconbutton.md)
- [Input](input.md)
- [InputOTP](inputotp.md)
- [Menubar](menubar.md)
- [Popover](popover.md)
- [Progress](progress.md)
- [RadioGroup](radiogroup.md)
- [ResizablePanelGroup](resizable.md)
- [Select](select.md)
- [Separator](separator.md)
- [Sheet](sheet.md)
- [Slider](slider.md)
- [Sonner](sonner.md)
- [Switch](switch.md)
- [Table](table.md)
- [Tabs](tabs.md)
- [Textarea](textarea.md)
- [TimePicker](timepicker.md)
- [Toast](toast.md)
- [Tooltip](tooltip.md)

---
examples: "extensions/fluent_ui"
example_images: "test-images/examples/extensions/fluent_ui/golden/macos"
title: "Fluent"
---

import {Image} from '@site/src/components/crocodocs';
import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';

# Fluent

Controls styled after Microsoft's [Fluent Design](https://fluent2.microsoft.design),
the design system of Windows, built on the Flutter
[`fluent_ui`](https://pub.dev/packages/fluent_ui) package, plus the
[`FluentIcons`](types/fluenticons.md) icon set.

## Usage

Add `flet-fluent-ui` to your project dependencies:

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```bash
uv add flet-fluent-ui
```

</TabItem>
<TabItem value="pip" label="pip">
```bash
pip install flet-fluent-ui  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
</TabItem>
</Tabs>

Then import it, typically under the `fluent` alias:

```python
import flet as ft
import flet_fluent_ui as fluent


def main(page: ft.Page):
    page.add(fluent.FilledButton("Continue"))


ft.run(main)
```

<Image src={frontMatter.example_images + '/overview/usage.png'} alt="usage" width="15%" caption="A Fluent filled button" />

## Theming

The controls work without any setup. A control that is not inside a
[`Theme`](theme.md) uses Fluent's default blue accent color and follows the
page's light or dark [`theme_mode`][flet.BasePage.theme_mode].

To use another accent color, a fixed brightness or a different font, wrap
controls in a [`Theme`](theme.md). Any color can be the accent color: the
lighter and darker shades for hover and pressed states are derived from it.

```python
fluent.Theme(
    accent_color=ft.Colors.PURPLE,
    content=ft.Column(
        [fluent.FilledButton("Save"), fluent.ToggleSwitch(label="Notify me", value=True)]
    ),
)
```

<Image src={frontMatter.example_images + '/overview/theming.png'} alt="theming" width="20%" caption="A purple accent color" />

Popups follow the `Theme` around the control that opens them, with one
exception. The lists of [`DatePicker`](datepicker.md) and
[`TimePicker`](timepicker.md), the calendar of
[`CalendarDatePicker`](calendardatepicker.md) and the menus of
[`DropDownButton`](dropdownbutton.md) and [`SplitButton`](splitbutton.md) use
the default blue accent color and the page's brightness.

## Icons

[`FluentIcons`](types/fluenticons.md) contains the Fluent icons. It can be used
anywhere Flet accepts an icon, including core controls such as
[`Icon`][flet.Icon] and [`IconButton`][flet.IconButton].

```python
ft.Row(
    tight=True,
    controls=[
        ft.Icon(fluent.FluentIcons.HOME),
        ft.Icon(fluent.FluentIcons.RINGER, color=ft.Colors.AMBER),
        ft.IconButton(fluent.FluentIcons.SETTINGS),
        fluent.IconButton(fluent.FluentIcons.HEART),
    ],
)
```

<Image src={frontMatter.example_images + '/overview/icons.png'} alt="icons" width="25%" caption="Fluent icons in core and Fluent controls" />

## Available controls

- [Theme](theme.md)
- [AutoSuggestBox](autosuggestbox.md)
- [BreadcrumbBar](breadcrumbbar.md)
- [Button](button.md)
- [CalendarDatePicker](calendardatepicker.md)
- [CalendarView](calendarview.md)
- [Card](card.md)
- [Checkbox](checkbox.md)
- [ColorPicker](colorpicker.md)
- [ComboBox](combobox.md)
- [CommandBar](commandbar.md)
- [ContentDialog](contentdialog.md)
- [ContextMenu](contextmenu.md)
- [DatePicker](datepicker.md)
- [Divider](divider.md)
- [DropDownButton](dropdownbutton.md)
- [Expander](expander.md)
- [FilledButton](filledbutton.md)
- [Flyout](flyout.md)
- [HyperlinkButton](hyperlinkbutton.md)
- [IconButton](iconbutton.md)
- [InfoBadge](infobadge.md)
- [InfoBar](infobar.md)
- [InfoLabel](infolabel.md)
- [ListTile](listtile.md)
- [MenuBar](menubar.md)
- [NavigationView](navigationview.md)
- [NumberBox](numberbox.md)
- [OutlinedButton](outlinedbutton.md)
- [PasswordBox](passwordbox.md)
- [ProgressBar](progressbar.md)
- [ProgressRing](progressring.md)
- [RadioGroup](radiogroup.md)
- [RatingBar](ratingbar.md)
- [ScaffoldPage](scaffoldpage.md)
- [Slider](slider.md)
- [SplitButton](splitbutton.md)
- [TabView](tabview.md)
- [TeachingTip](teachingtip.md)
- [TextBox](textbox.md)
- [TimePicker](timepicker.md)
- [ToggleButton](togglebutton.md)
- [ToggleSwitch](toggleswitch.md)
- [Tooltip](tooltip.md)
- [TreeView](treeview.md)

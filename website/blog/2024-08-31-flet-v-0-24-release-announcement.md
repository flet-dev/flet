---
slug: flet-v-0-24-release-announcement
title: Flet v0.24.0 Release Announcement
authors: henri
tags: [releases]
---

I am very happy to announce the release of Flet version 0.24.0! 
It comes with a very long list of bug fixes, several enhancements and new features.

<!-- truncate -->

## New Controls

- [`InteractiveViewer`](https://docs.flet.dev/controls/interactiveviewer/)
- [`Placeholder`](https://docs.flet.dev/controls/placeholder/)

## New Properties

- [`AudioRecorder`](https://docs.flet.dev/audio_recorder/): `cancel_recording()`
- [`Video`](https://docs.flet.dev/video/): `on_completed`, `on_track_changed`
- [`InputFilter`](https://docs.flet.dev/types/inputfilter/): `unicode`, `case_sensitive`, `dot_all`, `multiline`
- [`Geolocator`](https://docs.flet.dev/geolocator/): `on_error`, `on_position_change`
- [`Barchart`](https://docs.flet.dev/charts/bar_chart/), [`LineChart`](https://docs.flet.dev/charts/line_chart/): `tooltip_border_side`, `tooltip_direction`, `tooltip_fit_inside_horizontally`, `tooltip_fit_inside_vertically`, `tooltip_horizontal_offset`, `tooltip_margin`, `tooltip_max_content_width`, `tooltip_padding`, `tooltip_rounded_radius`, `tooltip_rotate_angle`
- [`Container`](https://docs.flet.dev/controls/container/): `decoration`, `foreground_decoration`, `ignore_interactions`, `image`
- [`Page`](https://docs.flet.dev/controls/page/), [`View`](https://docs.flet.dev/controls/view/): `decoration`, `foreground_decoration`
- [`CupertinoTextField`](https://docs.flet.dev/controls/cupertinotextfield/): `enable_scribble`, `image`, `obscuring_character`, `padding`, `scroll_padding`, `on_click`
- [`DataTable`](https://docs.flet.dev/controls/datatable/): `heading_row_alignment`
- [`TextField`](https://docs.flet.dev/controls/textfield/): `counter`, `disabled_hint_content`, `options_fill_horizontally`
- [`ExpansionTile`](https://docs.flet.dev/controls/expansiontile/): `min_tile_height`, `show_trailing_icon`
- [`Markdown`](https://docs.flet.dev/controls/markdown/): `fit_content`, `img_error_content`, `md_style_sheet`, `shrink_wrap`, `soft_line_break`, `on_selection_change`
- [`MenuItemButton`](https://docs.flet.dev/controls/menuitembutton/): `autofocus`, `overflow_axis`, `semantic_label`
- [`Tabs`](https://docs.flet.dev/controls/tabs/): `label_padding`, `label_text_style`, `padding`, `splash_border_radius`, `unselected_label_text_style`, `on_click`
- and lot of [new classes](https://docs.flet.dev/reference/) (enums, dataclasses, events)…

## Enhancements
- Better string output of Events when printed
- `Image.filter_quality` now has a default of `FilterQuality.MEDIUM` (previously `FilterQuality.LOW`), which is a better default for downscaled images.
- `Geolocator` control has been improved to support location streaming through the newly added on_position_change event. When defined, you will be able to "listen" to location changes as they happen.
- When `AppBar.adaptive=True` and the app is running on an Apple platform, the `AppBar.actions` controls are now wrapped in a `Row`, then displayed. Before this, only the first item of `AppBar.actions` list was displayed.
- The `Markdown` control has been significantly improved. It can now display SVG images and be much more customized.
- A very requested feature was the ability to set a background image or gradient for the application. In [#3820](https://github.com/flet-dev/flet/pull/3820), we made this possible and easy to use.
- rtl (right-to-left) property has been added to more controls (`NavigationRailDestination`, `NavigationRail`, `AppBar`, `CupertinoAppBar`, and `NavigationDrawer` ) to improve support for right-to-left text directions.
- Introduced `--no-rich-output` flag (only in `flet build` command for now) to make it possible to disable rich output (mainly emojis) in the console. More information in [#3708](https://github.com/flet-dev/flet/pull/3708).
- Typing has been significantly improved, particularly for event-handler properties. In modern IDEs like PyCharm and VSCode, you can now easily determine the type of an event handler's argument by simply hovering over the event in the control. Additionally, the IDE will highlight errors when you attempt to access a non-existent property on the event handler argument, ensuring more robust and error-free code.

## Bug Fixes

The below issues were successfully fixed:

- [#3769](https://github.com/flet-dev/flet/issues/3769): `InputFilter` clears the `TextField` text content when an invalid character is entered
- [#3770](https://github.com/flet-dev/flet/issues/3770): `Theme.floating_action_button_theme` non existent
- [#3734](https://github.com/flet-dev/flet/issues/3734): Ensure `Dropdown.alignment` is respected.
- [#3730](https://github.com/flet-dev/flet/issues/3730): `UnicodeEncodeError` raised when packaging on WindowOS
- [#2160](https://github.com/flet-dev/flet/issues/2160): `Markdown` control can't render svg images
- [#2158](https://github.com/flet-dev/flet/issues/2158): `Markdown` broken when an image is not found
- [#3679](https://github.com/flet-dev/flet/issues/3679): Broken `Dismissible`
- [#3670](https://github.com/flet-dev/flet/issues/3670): `Switch.height` and `Switch.width` not respected
- [#3612](https://github.com/flet-dev/flet/issues/3612), [#3566](https://github.com/flet-dev/flet/issues/3566): Broken `OnScrollEvent`
- [#3564](https://github.com/flet-dev/flet/issues/3564): Broken `TextField.capitalization`
- [#3649](https://github.com/flet-dev/flet/issues/3649): `CupertinoPicker` jumps-scroll on some platforms
- [#3557](https://github.com/flet-dev/flet/issues/3557): Impeller causes blank screen on mac Intel
- [#3574](https://github.com/flet-dev/flet/issues/3574): `Geolocator` not working on Android devices
- [#3505](https://github.com/flet-dev/flet/issues/3505): `WindowEventType` doesn't contain fullscreen all events

Thanks to all those who reported them!

## Deprecations

All deprecated items from this release will be removed in version 0.27.0.

- `ThemeVisualDensity` is deprecated and has been renamed to [`VisualDensity`](https://docs.flet.dev/types/visualdensity/)
- [`CupertinoButton`](https://docs.flet.dev/controls/cupertinobutton/): `disabled_color` is deprecated and has been renamed to `disabled_bgcolor`, which better reflects its use
- [`Markdown`](https://docs.flet.dev/controls/markdown/): `code_style` is deprecated and should now be accessed as  `code_style_sheet.code_text_style`
- [`Container`](https://docs.flet.dev/controls/container/): `image_fit`, `image_opacity`, `image_repeat`, `image_src` and `image_src_base64` are deprecated and should now be accessed from `image` which is of type [`DecorationImage`](https://docs.flet.dev/types/decorationimage/)

## Breaking Changes and Migration

### Tooltip
The Tooltip class is no more a Flet control and is from now on a simple Python dataclass. The tooltip property (available in almost all controls) now supports both strings and Tooltip objects.

Below is how to migrate:

```python
# before
page.add(
    ft.Tooltip(
        message="This is tooltip",
        content=ft.Text("Hover to see tooltip"),
        padding=20,
        border_radius=10,
    )
)

# after
page.add(
    ft.Text(
        "Hover to see tooltip",
        tooltip=ft.Tooltip(
            message="This is tooltip",
            padding=20,
            border_radius=10,
        )
    )
)
```

### TextField InputFilter
We modified how `InputFilter.regex_string` is internally handled. As a result of this, you (might) now have to anchor your regex pattern. This simply implies using start (^) and end ($) regex anchors.
For example: `r"[0-9]"` now becomes `r"^[0-9]$"`. Using this new string will lead work as expected and only numbers/digits will be allowed, but you might notice another issue: the last character of the text field cannot be deleted. To resolve this, you need to add an asterisk (*) in the regex which in this case will simply mean "match zero or more digits (including an empty string)". The new regex now becomes `r"^[0-9]*$"`.
To ease this migration, you can use an AI tool with the following simple prompt: `"update the following regex pattern: #### ensuring that the entire string matches the pattern and it allows for an empty string"`.

### Event-Handler subscription
The possibility to "subscribe" more than one callback to an event handler has been removed, as this was somehow biased (was only possible on some, and not all).
Below is a simple example:

```python
import flet as ft

def main(page: ft.Page):
    def print_one(e):
        print("1")
    def print_two(e):
        print("2")
    def print_three(e):
        print("3")
    c = ft.Container(
        bgcolor=ft.Colors.random_color(),
        width=300,
        height=300,
    )
    
    # subscribe callbacks
    c.on_tap_down = print_one
    c.on_tap_down = print_two
    c.on_tap_down = print_three
    page.add(c)

ft.run(main)
```

In the above code, we subscribe multiple callbacks to the [`Container.on_tap_down`](https://docs.flet.dev/controls/container/#flet.Container.on_tap_down) event. Prior to Flet version 0.24.0, running this code and tapping on the `Container`, you will see all the callbacks getting called ("1", "2" and "3" are printed out).
From Flet version 0.24.0 going forward, one event = one callback. Meaning only the lastly subscribed callback will get executed ("3" is printed out)
So, if you still want the final output to resemble the first one you can simply create one callback which calls the others:

```python

def main(page: ft.Page):
    #....
  
    def print_all(e):
            print_one(e)
            print_two(e)
            print_three(e)
    
    c = ft.Container(
            bgcolor=ft.Colors.random_color(),
            width=300,
            height=300,
            on_tap_down=print_all,
        )

    # OR
    c.on_tap_down = print_all
```

## Conclusion
As you can see, we made a lot of changes in this release and as usual, your feedback is highly welcomed!

Upgrade to Flet 0.24.0, test your apps and let us know how you find the new features we added.
If you have any questions, please join [Flet Discord server](https://discord.gg/dzWXP8SHG8) or create a new thread
on [Flet GitHub discussions](https://github.com/flet-dev/flet/discussions).

Happy Flet-ing! 👾

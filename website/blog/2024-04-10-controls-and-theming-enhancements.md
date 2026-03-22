---
slug: controls-and-theming-enhancements
title: Controls and theming enhancements
authors: henri
tags: [releases]
---

One month after the release of Flet 0.21.0, we are excited to announce the release of Flet 0.22.0.

This release comes with a lot of enhancements, bug fixes, and deprecations:

<!-- truncate -->

## Enhancements

This was one of the main concerns while coming up with this release. Two types of enhancements were made:

### Controls Enhancement

We went through the long list of already-present controls and exposed, where possible, more
properties - [PR #2882](https://github.com/flet-dev/flet/pull/2882). This will grant you more power/control over the
Flet Controls you use in your awesome applications.

Below is the complete list:

- [`AppBar`](https://docs.flet.dev/controls/appbar/): elevation_on_scroll, exclude_header_semantics,
  force_material_transparency, is_secondary, shadow_color, surface_tint_color, clip_behavior, title_spacing,
  toolbar_opacity, title_text_style, toolbar_text_style, shape
- [`AlertDialog`](https://docs.flet.dev/controls/alertdialog/): action_button_padding, clip_behavior, icon_padding,
  shadow_color, surface_tint_color
- [`Banner`](https://docs.flet.dev/controls/banner/): content_text_style, margin, elevation, divider_color, shadow_color,
  surface_tint_color, on_visible
- [`CupertinoListTile`](https://docs.flet.dev/controls/cupertinolisttile/): leading_size, leading_to_title
- [`CupertinoSegmentedButton`](https://docs.flet.dev/controls/cupertinosegmentedbutton/): click_color
- [`CupertinoSwitch`](https://docs.flet.dev/controls/cupertinoswitch/):on_label_color, off_label_color
- [`CupertinoTimerPicker`](https://docs.flet.dev/controls/cupertinotimerpicker/): item_extent
- [`Chip`](https://docs.flet.dev/controls/chip/): surface_tint_color, color, click_elevation, clip_behavior,
  visual_density, border_side
- [`Divider`](https://docs.flet.dev/controls/divider/): leading_indent, trailing_indent
- [`ExpansionTile`](https://docs.flet.dev/controls/expansiontile/): dense, enable_feedback, visual_density
- [`Card`](https://docs.flet.dev/controls/card/): clip_behavior, is_semantic_container, show_border_on_foreground,
  variant
- [`Checkbox`](https://docs.flet.dev/controls/checkbox/): border_side, semantics_label, shape, splash_radius, is_error,
  visual_density, mouse_cursor
- [`CircleAvatar`](https://docs.flet.dev/controls/circleavatar/): on_image_error
- [`DataTable`](https://docs.flet.dev/controls/datatable/): clip_behavior
- [`DatePicker`](https://docs.flet.dev/controls/datepicker/): on_entry_mode_change
- [`Draggable`](https://docs.flet.dev/controls/draggable/): on_drag_complete, on_drag_start
- [`DragTarget`](https://docs.flet.dev/controls/dragtarget/): on_move
- [`Dropdown`](https://docs.flet.dev/controls/dropdown/): fill_color, hint_content, icon_content, elevation, item_height,
  max_menu_height, icon_size, enable_feedback, padding, icon_enabled_color, icon_disabled_color, on_click
- [`ElevatedButton`](https://docs.flet.dev/controls/elevatedbutton/): clip_behavior
- [`FloatingActionButton`](https://docs.flet.dev/controls/floatingactionbutton/): clip_behavior, enable_feedback,
  focus_color, foreground_color, disabled_elevation, elevation, focus_elevation, highlight_elevation, hover_elevation,
  mouse_cursor
- [`GridView`](https://docs.flet.dev/controls/gridview/): cache_extent, clip_behavior, semantic_child_count
- [`IconButton`](https://docs.flet.dev/controls/iconbutton/): alignment, disabled_color, focus_color, enable_feedback,
  hover_color, padding, splash_color, splash_radius, focus_color, mouse_cursor, visual_density
- [`Image`](https://docs.flet.dev/controls/image/): exclude_from_semantics, filter_quality
- [`ListTile`](https://docs.flet.dev/controls/listtile/): enable_feedback, horizontal_spacing, min_leading_width,
  min_vertical_padding, selected_color, selected_tile_color, style, title_alignment, icon_color, text_color, shape,
  visual_density, mouse_cursor, title_text_style, subtitle_text_style, leading_and_trailing_text_style
- [`ListView`](https://docs.flet.dev/controls/listview/): cache_extent, clip_behavior, semantic_child_count
- [`NavigationBar`](https://docs.flet.dev/controls/navigationbar/): animation_duration, overlay_color
- [`NavigationDrawerDestination`](https://docs.flet.dev/controls/navigationdrawer/): bgcolor
- [`NavigationBarDestination`](https://docs.flet.dev/controls/navigationbardestination/): bgcolor
- [`NavigationRail`](https://docs.flet.dev/controls/navigationrail/): selected_label_text_style,
  unselected_label_text_style
- [`NavigationRailDestination`](https://docs.flet.dev/controls/navigationrail/): indicator_color, indicator_shape
- [`Option`](https://docs.flet.dev/controls/dropdownoption/#flet.DropdownOption): alignment, on_click
- [`OutlinedButton`](https://docs.flet.dev/controls/outlinedbutton/): clip_behavior
- [`Page`](https://docs.flet.dev/controls/page/): locale_configuration
- [`PopupMenuItem`](https://docs.flet.dev/controls/popupmenubutton/#flet.PopupMenuItem): height, padding,
  mouse_cursor
- [`PopupMenuButton`](https://docs.flet.dev/controls/popupmenubutton/): bgcolor, clip_behavior, elevation,
  enable_feedback, icon_color, shadow_color, surface_tint_color, icon_size, padding, splash_radius, shape, on_open,
  on_cancel
- [`ProgressBar`](https://docs.flet.dev/controls/progressbar/): border_radius, semantics_label, semantics_value
- [`ProgressRing`](https://docs.flet.dev/controls/progressring/): semantics_label, semantics_value, stroke_cap,
  stroke_align
- [`Radio`](https://docs.flet.dev/controls/radio/): focus_color, hover_color, overlay_color, splash_radius, toggleable,
  visual_density, mouse_cursor
- [`SearchBar`](https://docs.flet.dev/controls/searchbar/): keyboard_type, view_surface_tint_color, autofocus
- [`SelectionArea`](https://docs.flet.dev/controls/selectionarea/): on_change
- [`Slider`](https://docs.flet.dev/controls/slider/): interaction, overlay_color, mouse_cursor, secondary_track_value,
  secondary_active_color
- [`Stack`](https://docs.flet.dev/controls/stack/): alignment, fit
- [`SnackBar`](https://docs.flet.dev/controls/snackbar/): clip_behavior, shape, on_visible, action_overflow_threshold
- [`Switch`](https://docs.flet.dev/controls/switch/): hover_color, splash_radius, overlay_color, track_outline_color,
  mouse_cursor
- [`Tabs`](https://docs.flet.dev/controls/tabs/): divider_height, enable_feedback, indicator_thickness, is_secondary,
  mouse_cursor, clip_behavior
- [`TextField`](https://docs.flet.dev/controls/textfield/): fill_color, hover_color
- [`TimePicker`](https://docs.flet.dev/controls/timepicker/): orientation, on_entry_mode_change
- [`Tooltip`](https://docs.flet.dev/types/tooltip/): enable_tap_to_dismiss, exclude_from_semantics
- [`VerticalDivider`](https://docs.flet.dev/controls/verticaldivider/): leading_indent, trailing_indent

If you however feel that something lacks and should be added, don't hesitate to let us know.

Check out the article I wrote
concerning `Page.locale_configuration` [here](https://ndonkohenri.medium.com/app-localization-in-flet-5b523e83ca89).

### Theme Enhancements

The Theme class which is used for application theming in light and dark mode has equally been further enhanced.
Lots of new themes were introduced - [PR #2955](https://github.com/flet-dev/flet/pull/2955).

See the Theming Guide [here](https://docs.flet.dev/cookbook/theming/).

## Rive Animations

[Rive](https://rive.app/) is a very popular real-time interactive design and animation tool.
The newly introduced [`Rive`](https://docs.flet.dev/rive/) Control allows you to load and visualize any Rive
animation in your applications.

The animation's source (`Rive.src`) can either be a local asset file or a URL - as usual, it all depends on your needs.

## Parent Control

As requested in [#952](https://github.com/flet-dev/flet/issues/952), the ability to access the parent of any control has
been added: `Control.parent`.

Read more on it [here](https://ndonkohenri.medium.com/access-any-controls-parent-flet-98e2c60dfab8).

## Bug Fixes

The below issues were successfully fixed:

- [#2560](https://github.com/flet-dev/flet/issues/2560) - `Dropdown.bgcolor` was not visually respected
- [#2740](https://github.com/flet-dev/flet/issues/2740) - `CircleAvatar` not working with local asset images
- [#2781](https://github.com/flet-dev/flet/issues/2781) - `'FletSocketServer'` Error raised on Linux
- [#2826](https://github.com/flet-dev/flet/issues/2826) - `PopupMenuItem.data` not respected
- [#2839](https://github.com/flet-dev/flet/issues/2839) - `ExpansionTile.initially_expanded` had no visual effect
- [#2867](https://github.com/flet-dev/flet/issues/2867) - `PopupMenuButton` had an always-visible tooltip of "Show menu"
- On some Python versions, you might have seen a RuntimeError('Event loop is closed') which usually shows up when
  closing the app's window. The Python-dev
  team [fixed](https://github.com/python/cpython/issues/109538#issuecomment-1823306415) this asyncio-related issue
  recently, but this fix is only present in the versions released from the year 2024. So if you face this issue,
  please [download](https://www.python.org/downloads/) one of the latest Python releases and replace the one used in
  your environment.

Special Thanks to the dynamic Flet community for reporting all the issues they encountered. We keep working hard on
solving the remaining ones.

## Deprecations

As previously mentioned in the [announcement](https://python.plainenglish.io/whats-new-in-flet-0-21-0-ca482ab4520b)
concerning Flet v0.21.0, all deprecations will be completely removed from the API in version 1.0 - so you have enough
time to update your apps.

You must not completely memorize what has been deprecated as we've added DeprecationWarnings which will be shown
directly in your console (without breaking your app).

- [`PopupMenuButton.on_cancelled`](https://docs.flet.dev/controls/popupmenubutton/#flet.PopupMenuButton.on_cancel) has been renamed
  to [`on_cancel`](https://docs.flet.dev/controls/popupmenubutton/#flet.PopupMenuButton.on_cancel)
- [`foreground_image_url`](https://docs.flet.dev/controls/circleavatar/#flet.CircleAvatar.foreground_image_src)
  and [`background_image_url`](https://docs.flet.dev/controls/circleavatar/#flet.CircleAvatar.background_image_src) properties
  of [`CircleAvatar`](https://docs.flet.dev/controls/circleavatar/) were renamed
  to [`foreground_image_src`](https://docs.flet.dev/controls/circleavatar/#flet.CircleAvatar.foreground_image_src)
  and [`background_image_src`](https://docs.flet.dev/controls/circleavatar/#flet.CircleAvatar.background_image_src) respectively
- `DragTargetAcceptEvent` used in the [`DragTarget.on_accept`](https://docs.flet.dev/controls/dragtarget/#flet.DragTarget.on_accept) has
  been renamed to `DragTargetEvent`

## Documentation

The Flet documentation has been reorganized to ease navigation (especially for beginners/new users).

Upgrade to Flet 0.22.0, test your apps and let us know how you find the new features we added.
If you have any questions, please join [Flet Discord server](https://discord.gg/dzWXP8SHG8) or create a new thread
on [Flet GitHub discussions](https://github.com/flet-dev/flet/discussions).

Happy Flet-ing!

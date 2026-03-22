---
slug: flet-v-0-23-release-announcement
title: Flet v0.23.0 Release Announcement
authors: henri
tags: [releases]
---

We are excited to announce the release of Flet 0.23.0. It is a big release with many new features and bug fixes.

<!-- truncate -->

## New Controls

- [`AutoComplete`](https://docs.flet.dev/controls/autocomplete/)
- [`AutoFillGroup`](https://docs.flet.dev/controls/autofillgroup/)
- [`Flashlight`](https://docs.flet.dev/flashlight/)
- [`Geolocator`](https://docs.flet.dev/geolocator/)
- [`Map`](https://docs.flet.dev/map/)
- [`PermissionHandler`](https://docs.flet.dev/permission_handler/)

## New Properties

- [`Option`](https://docs.flet.dev/controls/dropdownoption/#flet.DropdownOption): `content`, `text_style`
- [`TextStyle`](https://docs.flet.dev/types/textstyle/): `baseline`, `overflow`, `word_spacing`

## Error Handling

> PEP 20 (Zen of Python): Errors should never pass silently.

Several devs reported that, on some occasions, a control might visually break without clear information on what caused
the break.

For example, in issue [#3149](https://github.com/flet-dev/flet/issues/3149), @base-13 mentioned that _"in a DataTable if
the number of columns is less than the number of datacells in any row it will grey out whole table without throwing
error"_.

Knowing this, we added more assertion-checks in most of the controls, such that, when you provide them with a wrong
value, an AssertionError is raised with a very clear message of what was wrongly done.

If you find out that some checks are still missing, please point them out so they can be addressed.

## Command Line (CLI) Output

The output of the `flet build` command has been prettified.

Also, a new option has been added --show-platform-matrix which displays a table containing the build platform matrix,
which has header columns "Command" (possible build commands) and "Platform" (the device you should use with the
respective command).

Furthermore, when the targeted platform can't be built on your device, a table displaying the build platform matrix is
shown with an informative message.

## Breaking Changes

While doing "Error Handling" mentioned above, we had to mark some important properties as required.

The following properties are now "required" (must be provided and visible) when creating an instance of their classes:

* [`AnimatedSwitcher.content`](https://docs.flet.dev/controls/animatedswitcher/#flet.AnimatedSwitcher.content)
* [`Banner.content`](https://docs.flet.dev/controls/banner/#flet.Banner.content), [`Banner.actions`](https://docs.flet.dev/controls/banner/#flet.Banner.actions)
* [`BottomSheet.content`](https://docs.flet.dev/controls/bottomsheet/#flet.BottomSheet.content)
* [`CupertinoActionSheetAction.content`](https://docs.flet.dev/controls/cupertinoactionsheetaction/#flet.CupertinoActionSheetAction.content)
* [`DataRow.cells`](https://docs.flet.dev/controls/datatable/)
* [`DataTable.columns`](https://docs.flet.dev/controls/datatable/)
* [`DragTarget.content`](https://docs.flet.dev/controls/dragtarget/#flet.DragTarget.content)
* [`Draggable.content`](https://docs.flet.dev/controls/draggable/#flet.Draggable.content)
* [`ExpansionTile.title`](https://docs.flet.dev/controls/expansiontile/#flet.ExpansionTile.title)
* [`MenuBar.controls`](https://docs.flet.dev/controls/menubar/#flet.MenuBar.controls)
* [`Pagelet.content`](https://docs.flet.dev/controls/pagelet/#flet.Pagelet.content)
* [`RadioGroup.content`](https://docs.flet.dev/controls/radio/#flet.Radio.content)
* [`SafeArea.content`](https://docs.flet.dev/controls/safearea/#flet.SafeArea.content)
* [`ShaderMask.shader`](https://docs.flet.dev/controls/shadermask/#flet.ShaderMask.shader)
* [`WindowDragArea.content`](https://docs.flet.dev/controls/windowdragarea/#flet.WindowDragArea.content)

## Bug Fixes

The below issues were successfully fixed:

* [#3144](https://github.com/flet-dev/flet/issues/3144): `ScrollbarTheme.thickness` value not respected when not
  interacting with
* [#3072](https://github.com/flet-dev/flet/issues/3072): High-resolution videos play laggy on Android TV devices.
* [#3023](https://github.com/flet-dev/flet/issues/3023): (Regression) Some `LineChart` colors not visually respected
* [#2989](https://github.com/flet-dev/flet/issues/2989): Color of [`Dropdown`](https://docs.flet.dev/controls/dropdown/) when disabled
  doesn't reflect its disabled state
* [#1753](https://github.com/flet-dev/flet/issues/1753): [`Markdown`](https://docs.flet.dev/controls/markdown/) code block not selectable
* [#3097](https://github.com/flet-dev/flet/issues/3097): Hot-reload occurs when a file is opened
* [#1647](https://github.com/flet-dev/flet/issues/1647): [`Container.theme_mode`](https://docs.flet.dev/controls/container/#flet.Container.theme_mode)
  not honoured when `Container.theme=None`
* [#3064](https://github.com/flet-dev/flet/issues/3064): [`Container.on_tap_down`](https://docs.flet.dev/controls/container/#flet.Container.on_tap_down)
  not called when `Container.on_click=None`

Special Thanks to the dynamic Flet community for reporting all the issues they encountered. We keep working hard on
solving the remaining ones.

## Deprecations

* All the `Page.window_***` properties are now deprecated and moved to [`Page.window`](https://docs.flet.dev/controls/page/#flet.Page.window)
  property, which is of type [`Window`](https://docs.flet.dev/types/window/).
  To migrate, simply use change `window_` to `window.` as seen below:
  ```python
  # before 
  page.window_height = 200
  page.on_window_event = lambda e: print(e.type)
  
  # now
  page.window.height = 200
  page.window.on_event = lambda e: print(e.type)
  ```

* `SafeArea.minimum` is deprecated and has been renamed
  to [`minimum_padding`](https://docs.flet.dev/controls/safearea/#flet.SafeArea.minimum_padding)
* `MaterialState` enum is deprecated and has been renamed to [`ControlState`](https://docs.flet.dev/types/controlstate/)
* `NavigationDestination` is deprecated and has been renamed
  to [`NavigationBarDestination`](https://docs.flet.dev/controls/navigationbardestination/#flet.NavigationBarDestination)

Also, the deprecation policy has been modified. While Flet is pre-1.0, all deprecations will be removed from the API after the next 3 releases.
So the above deprecations made in v0.23.0 (and all the other deprecations made in the previous versions), will be removed in v0.26.0.

That's it! :)

Upgrade to Flet 0.23.0, test your apps and let us know how you find the new features we added.
If you have any questions, please join [Flet Discord server](https://discord.gg/dzWXP8SHG8) or create a new thread
on [Flet GitHub discussions](https://github.com/flet-dev/flet/discussions).

Happy Flet-ing!

---
title: "Extensions: properties sent from Dart must be declared"
---

# Extensions: properties sent from Dart must be declared

:::note
This guide is accurate as of Flet 1.1.3. Later releases might add new APIs or
additional migration paths.

The [breaking changes and deprecations index](../index.md) lists the guides created for each release.
:::

## Summary

Starting with Flet 1.1.3, Python applies a property that a control's Dart code sends
with `updateProperties()` only if the control lists it in the `client_writable` argument
of its `@ft.control` decorator. Every other property sent by a client is ignored.

All controls that ship with Flet declare theirs. A control from an extension has to do
the same if its Dart code sends values to Python. Without the declaration, the widget
shows the new value, but the Python field keeps the old one. For example,
`e.control.value` is out of date in an event handler.

Flet logs a warning, once per control class and field, when it ignores a value for a field
that the control has but doesn't list in `client_writable`:

```text
Ignored a value a client sent for Rating.stars. If the control's Dart code updates this property, add it to `client_writable` in the @control decorator.
```

Events need no declaration: an extension's `on_*` handlers receive the events its Dart
code triggers, except in the cases listed under [Other changes](#other-changes).

## Background

A client decides what it sends, and on the web anyone can connect one. Python used to
apply every property it received, including private attributes and fields no widget ever
updates, such as `Control.data`, `Page.client_ip` and the state behind `Page.auth`. It also
changed value objects in place, including ones an app shares between sessions, and ran any
event on any control. Apps could therefore be made to run a handler on state chosen by the
client.

## Migration guide

List the fields your Dart code sends in `client_writable`. For example, with this widget:

```dart
widget.control.updateProperties({"stars": stars});
```

declare `stars` on the Python control:

```python
@ft.control("Rating", client_writable=("stars",))
class Rating(ft.LayoutControl):
    stars: int = 0
```

Subclasses inherit the lists and can extend them. A `client_writable` name that isn't a
field of the control, an `enabled_only` name that is neither a field nor an event, or a
`server_events` name without a matching `on_` field raises `ValueError` when the class is
defined.

If your Dart code holds back a value or an event while the control is disabled, list it in
`enabled_only` as well, and Python ignores it from a client in that state:

```python
from typing import Optional

import flet as ft


@ft.control("Rating", client_writable=("stars",), enabled_only=("change", "stars"))
class Rating(ft.LayoutControl):
    stars: int = 0
    on_change: Optional[ft.ControlEventHandler["Rating"]] = None
```

An extension using these arguments needs `flet>=1.1.3`.

Controls written only in Python need no change.

## Other changes

These affect what a client can do, and may matter to an app:

- **Hidden controls.** Python ignores what a client sends for a control that has
  `visible=False`, is inside one, or is inside a closed dialog. The exceptions are the
  `blur`, `dismiss`, `drag_complete`, `animation_end`, `size_change`, `hover`, `enter` and
  `exit` events, and `open` for a dialog that is closing. `Page.visible` has no effect, as
  on the client, and a service or the `Window` is never treated as hidden.
- **Disabled controls.** For the controls that declare it, Python ignores the events and
  values their widget holds back while the control or an ancestor is disabled, such as
  `click` and `long_press` of a button, or `value` and `change` of a `TextField`. Widgets
  that keep working while disabled, such as `GestureDetector`, `SearchBar`, `AutoComplete`
  and the date and time pickers, are unaffected.
- **Read-only controls.** Python ignores `value` and `change` for a control with
  `read_only=True`.
- **Dialogs.** A client can close a dialog, but not open one.
- **Events only Python triggers.** Python ignores `connect`, `disconnect`, `close`,
  `login`, `logout` and `views_pop_until` on the page when they come from a client. An
  extension can list its own with the `server_events` argument of `@ft.control`.
- **Values of the wrong type.** Python ignores a `dict` or `list` sent for a field that
  holds a single value.
- **Values and events on their way.** A click or a value already on its way when a handler
  disables or hides the control is ignored, and this goes by the state in Python, even if
  the client hasn't received it yet: call `update()` before a long `await` after disabling a
  field. For a value, the client gets the server's value back, so the widget and the Python
  field stay the same.
- **Nested values.** A client's update of a nested value, such as `Page.media` or
  `TextField.selection`, replaces it with a copy, so a shared object is never changed.
  Read `page.media` when you need it instead of keeping a reference to it. In declarative
  apps, a value object declared as a constant is sent again on the next render, like any
  other declared value.
- **Client-supplied ids.** `DragTargetEvent.src` is `None` unless the source is a
  `Draggable`, in the same group for an accepted drop. `ContextMenuSelectEvent.item` is
  `None` unless the item belongs to that menu.

These rules follow what a real client does, so they don't replace authorization in your
app. See [Security](../../../publish/web/dynamic-website/index.md#security).

## Timeline

- Changed in: `1.1.3`

## References

- Docs: [Sending values to Python](../../../extend/user-extensions.md#sending-values-to-python)
- Release notes: [Flet 1.1.3](../../release-notes.md)

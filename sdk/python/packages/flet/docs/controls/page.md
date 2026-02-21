---
class_name: flet.Page
examples: ../../examples/controls/page
example_images: ../examples/controls/page/media
---

{{ class_summary(class_name) }}

## Examples

### Listening to keyboard events

```python
--8<-- "{{ examples }}/keyboard_events.py"
```

### Mobile device orientation configuration

Shows how to lock your app to specific device orientations
(e.g., portrait up, landscape right) and listen for orientation changes on mobile devices.

```python
--8<-- "{{ examples }}/device_orientation.py"
```

### App exit confirmation

```python
--8<-- "{{ examples }}/app_exit_confirm_dialog.py"
```

### Hidden app window on startup

A Flet desktop app (Windows, macOS, or Linux) can start with its window hidden.
This lets your app perform initial setup (for example, add content, resize
or position the window) before showing it to the user.

In the example below, the window is resized and centered before becoming visible:

```python
--8<-- "{{ examples }}/window_hidden_on_start.py"
```

If you need this feature when packaging a desktop app using
[`flet build`](../cli/flet-build.md), see [this](../publish/index.md#hidden-app-window-on-startup).

### Toggle semantics debugger

```python
--8<-- "{{ examples }}/semantics_debugger.py"
```

### Get device locales

```python
--8<-- "{{ examples }}/device_locale.py"
```

{{ class_members(class_name) }}

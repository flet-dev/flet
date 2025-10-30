---
class_name: flet.ContextMenu
examples: ../../examples/controls/context_menu_region
---

{{ class_summary(class_name) }}

> Tip: On the web, call `await page.browser_context_menu.disable()` to suppress the
> default browser menu before relying on custom menus. Handlers receive a
> [`ContextMenuEvent`][flet.ContextMenuEvent] with the pointer location, trigger
> button, and selection metadata.

## Examples

```python
--8<-- "{{ examples }}/basic.py"
```

## Programmatic open

```python
await region.open(
    button=ft.ContextMenuButton.SECONDARY,
    local_position=(120, 40),
)
```

{{ class_members(class_name) }}

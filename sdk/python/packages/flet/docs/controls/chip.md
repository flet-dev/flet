::: flet.Chip

## Examples

[Live example](https://flet-controls-gallery.fly.dev/input/chip)

### Assist chips

Assist chips are chips with [`leading`][flet.Chip.leading] icon and [`on_click`][flet.Chip.on_click] event specified.

They represent smart or automated actions that appear dynamically and contextually in a UI.

An alternative to assist chips are [buttons](buttons/index.md), which should appear persistently and consistently.

```python
--8<-- "https://raw.githubusercontent.com/flet-dev/examples/refs/heads/v1-docs/python/controls/chip/assist-chips.py"
```

![assist-chips](https://raw.githubusercontent.com/flet-dev/examples/v1-docs/python/controls/chip/media/assist-chips.png){width="80%"}
/// caption
///

### Filter chips

Filter chips are chips with [`on_select`][flet.Chip.on_select] event specified.

They use tags or descriptive words provided in the [`label`][flet.Chip.label] to filter content.
They can be a good alternative to switches or checkboxes.

```python
--8<-- "https://raw.githubusercontent.com/flet-dev/examples/refs/heads/v1-docs/python/controls/chip/filter-chips.py"
```

![filter-chips](https://raw.githubusercontent.com/flet-dev/examples/v1-docs/python/controls/chip/media/filter-chips.png){width="80%"}
/// caption
///

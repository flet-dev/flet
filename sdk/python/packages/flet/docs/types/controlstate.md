{{ class_all_options("flet.ControlState") }}

## Usage Example

Configuring `fill_color` can be done in two ways:

### 1. Single Value for All States

If you want to use the same color across all Material states, simply assign `fill_color` to a single color:

```python
ft.Radio(fill_color=ft.Colors.GREEN)
```

### 2. Specific Values for Each State

For more control, you can provide a dictionary where the key is the state name and the value is the corresponding color.

#### **Ordering Matters**

- The order in which states appear in the dictionary will determine their priority, allowing for flexibility and
  customization.
- The position of `DEFAULT` does not affect behavior—it always has the least priority and can be placed anywhere in the
  dictionary.

#### **Example**

To configure different fill colors of a [`Radio`][flet.Radio] button for `ControlState.HOVERED` and
`ControlState.FOCUSED`, with a fallback color for all other states:

```python
ft.Radio(
    fill_color={
        ft.ControlState.HOVERED: ft.Colors.GREEN,
        ft.ControlState.FOCUSED: ft.Colors.RED,
        ft.ControlState.DEFAULT: ft.Colors.BLACK,
    }
)
```

This setup ensures that `HOVERED` and `FOCUSED` states take precedence, while all unspecified states default to `BLACK`.

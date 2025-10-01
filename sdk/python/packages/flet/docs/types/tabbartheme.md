{{ class_all_options("flet.TabBarTheme") }}

## Examples

### Example 1

```python
page.theme = ft.Theme(
    tabs_theme=ft.TabBarTheme(
        divider_color=ft.Colors.BLUE,
        indicator_color=ft.Colors.RED,
        indicator_tab_size=True,
        label_color=ft.Colors.GREEN,
        unselected_label_color=ft.Colors.AMBER,
        overlay_color={
            ft.MaterialState.FOCUSED: ft.Colors.with_opacity(0.2, ft.Colors.GREEN),
            ft.MaterialState.DEFAULT: ft.Colors.with_opacity(0.2, ft.Colors.PINK),
        },
    )
)
```

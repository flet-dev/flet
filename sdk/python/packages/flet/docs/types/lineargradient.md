::: flet.LinearGradient

### Usage example

<img src="/img/docs/controls/container/linear-gradient.png" className="screenshot-20" />

```python
Container(
    gradient=ft.LinearGradient(
        begin=ft.alignment.top_center,
        end=ft.alignment.bottom_center,
       colors=[ft.Colors.BLUE, ft.Colors.YELLOW],
    ),
    width=150,
    height=150,
    border_radius=5,
)
```
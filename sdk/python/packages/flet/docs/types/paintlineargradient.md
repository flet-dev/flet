::: flet.PaintLinearGradient

## Usage example

<img src="/img/docs/controls/canvas/paint-linear-gradient.png" className="screenshot-20" />

```python
cv.Rect(
    10,
    10,
    100,
    100,
    5,
    ft.Paint(
        gradient=ft.PaintLinearGradient(
            (0, 10), (0, 100), colors=[ft.Colors.BLUE, ft.Colors.YELLOW]
        ),
        style=ft.PaintingStyle.FILL,
    ),
)
```
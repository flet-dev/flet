::: flet.PaintRadialGradient

## Usage example

<img src="/img/docs/controls/canvas/paint-radial-gradient.png" className="screenshot-20" />

```python
cv.Circle(
    60,
    170,
    50,
    ft.Paint(
        gradient=ft.PaintRadialGradient(
            (60, 170), 50, colors=[ft.Colors.YELLOW, ft.Colors.BLUE]
        ),
        style=ft.PaintingStyle.FILL,
    ),
)
```
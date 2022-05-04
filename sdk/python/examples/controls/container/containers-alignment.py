import flet
from flet import Container, ElevatedButton, Page, Row, alignment, colors


def main(page: Page):
    page.title = "Containers with different alignments"

    c1 = Container(
        content=ElevatedButton("Center"),
        bgcolor=colors.AMBER,
        padding=15,
        alignment=alignment.center,
        width=150,
        height=150,
    )

    c2 = Container(
        content=ElevatedButton("Top left"),
        bgcolor=colors.AMBER,
        padding=15,
        alignment=alignment.top_left,
        width=150,
        height=150,
    )

    c3 = Container(
        content=ElevatedButton("-0.5, -0.5"),
        bgcolor=colors.AMBER,
        padding=15,
        alignment=alignment.Alignment(-0.5, -0.5),
        width=150,
        height=150,
    )

    r = Row([c1, c2, c3])
    page.add(r)


flet.app(target=main)

# bottom_center = Alignment(0, 1)
# bottom_left = Alignment(-1, 1)
# bottom_right = Alignment(1, 1)
# center = Alignment(0, 0)
# center_left = Alignment(-1, 0)
# center_right = Alignment(1, 0)
# top_center = Alignment(0, -1)
# top_left = Alignment(-1, -1)
# top_right = Alignment(1, -1)


# - bgColor (background color - `decoration: BoxDecoration.color`)
# - alignment - `topLeft`, `topCenter`, `topRight`, `centerLeft`, `center`, `centerRight`, `bottomLeft`, `bottomCenter`, `bottomRight`
# - border - width, color
# - borderRadius
# - verticalScroll (S2)
# - horizontalScroll (S2)
# - autoScroll (S2) - `end`, `start` ([example](https://stackoverflow.com/questions/43485529/programmatically-scrolling-to-the-end-of-a-listview)).
# - content - child control of any type
# - margin
# - padding
# - tooltip

# Common Properties:

# - visible
# - disabled

# - expand (int) - The control is forced to fill the available space inside Row or Column. Flex factor specified by the property. Default is 1. The property has affect only for direct descendants of Row and Column controls. (Wrap control into Expanded).
# - flex (S2) (int) - The child can be at most as large as the available space (but is allowed to be smaller) inside Row or Column. Flex factor specified by the property. Default is 1. The property has affect only for direct descendants of Row and Column controls. (Wrap control into Flexible with fit=FlexFit.loose).

# The only difference if you use Flexible instead of Expanded, is that Flexible lets its child have the same or smaller width than the Flexible itself, while Expanded forces its child to have the exact same width of the Expanded. But both Expanded and Flexible ignore their children’s width when sizing themselves.

# - width - wrap into SizedBox
# - height - wrap into SizedBox
# - minHeight (S2) - wrap into ConstrainedBox
# - maxHeight (S2) - wrap into ConstrainedBox
# - minWidth (S2) - wrap into ConstrainedBox
# - maxWidth (S2) - wrap into ConstrainedBox

# - fit (S2)
# - fitAlign (S2) - Wrap into FittedBox

# - opacity - allows to specify transparency of the control, hide it completely or blend with another if used with Stack. 0.0 - hidden, 1.0 - fully visible. See https://api.flutter.dev/flutter/widgets/Opacity-class.html.

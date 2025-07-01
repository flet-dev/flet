::: flet.SegmentedButton

## Examples

[Live example](https://flet-controls-gallery.fly.dev/buttons/segmentedbutton)



```python
import flet as ft


def main(page: ft.Page):
    def handle_change(e):
        print("on_change data : " + str(e.data))

    page.add(
        ft.SegmentedButton(
            on_change=handle_change,
            selected_icon=ft.Icon(ft.Icons.ONETWOTHREE),
            selected={"1", "4"},
            allow_multiple_selection=True,
            segments=[
                ft.Segment(
                    value="1",
                    label=ft.Text("1"),
                    icon=ft.Icon(ft.Icons.LOOKS_ONE),
                ),
                ft.Segment(
                    value="2",
                    label=ft.Text("2"),
                    icon=ft.Icon(ft.Icons.LOOKS_TWO),
                ),
                ft.Segment(
                    value="3",
                    label=ft.Text("3"),
                    icon=ft.Icon(ft.Icons.LOOKS_3),
                ),
                ft.Segment(
                    value="4",
                    label=ft.Text("4"),
                    icon=ft.Icon(ft.Icons.LOOKS_4),
                ),
            ],
        )
    )


ft.run(main)
```


<img src="/img/docs/controls/segmented-button/segmented-button.png" className="screenshot-40" />

## `SegmentedButton` Properties

### `allow_empty_selection`

A boolean value that indicates if having no selected segments is allowed. 

If `True`, then it is acceptable for none of the segments to be selected and also that `selected` can be empty.

If `False` (the default), there must be at least one segment selected. If the user taps on the only selected segment it will not be deselected, and `on_change` will not be called.

### `allow_multiple_selection`

A boolean value that indicates if multiple segments can be selected at one time.

If `True`, more than one segment can be selected. When selecting a segment, the other `selected` segments will stay selected. Selecting an already selected segment will unselect it.

If `False`(the default), only one segment may be selected at a time. When a segment is selected, any previously selected segment will be unselected.

### `direction`

The orientation of the button's `segments`. 

Value is of type [`Axis`](/docs/reference/types/axis) and defaults to `Axis.HORIZONTAL`.

### `padding`

Defines the button's size and padding. If specified, the button expands to fill its parent's space with this padding.

When `None`, the button adopts its intrinsic content size.

Value is of type [`PaddingValue`](/docs/reference/types/aliases#paddingvalue).

### `segments`

A required parameter that describes the segments in the button. It's a list of `Segment` objects.

### `selected`

A set of `Segment.value`s that indicate which segments are selected. It is updated when the user (un)selects a segment.

### `selected_icon`

An `Icon` control that is used to indicate a segment is selected.

If `show_selected_icon` is `True` then for `selected` segments this icon will be shown before the `Segment.label`, replacing the `Segment.icon` if it is specified.

Defaults to an `Icon` with the `CHECK` icon.

### `show_selected_icon`

A boolean value that indicates if the `selected_icon` is displayed on the `selected` segments.

If `True`, the `selected_icon` will be displayed at the start of the `selected` segments.

If `False`, then the `selected_icon` is not used and will not be displayed on `selected` segments.

### `style`

Customizes this button's appearance.

Value is of type [`ButtonStyle`](/docs/reference/types/buttonstyle).

## Events

### `on_change`

Fires when the selection changes.

## `Segment` Properties

### `disabled`

Determines if the segment is available for selection.

### `icon`

The icon (typically an [`Icon`](/docs/controls/icon)) to be displayed in the segment.

### `label`

The label (usually a [`Text`](/docs/controls/text)) to be displayed in the segment.

### `tooltip`

The tooltip for the segment.

### `value`

Used to identify the `Segment`.






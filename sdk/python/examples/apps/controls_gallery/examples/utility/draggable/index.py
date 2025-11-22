name = "Draggable / DragTarget"

description = """Draggable is a control that can be dragged from to a DragTarget.

When a draggable control recognizes the start of a drag gesture, it displays a content_feedback control that tracks the user's finger across the screen. If the user lifts their finger while on top of a DragTarget, that target is given the opportunity to complete drag-and-drop flow.

This control displays content when zero drags are under way. If content_when_dragging is non-null, this control instead displays content_when_dragging when one or more drags are underway. Otherwise, this widget always displays `content`.


DragTarget is a control that completes drag operation when a Draggable widget is dropped.

When a draggable is dragged on top of a drag target, the drag target is asked whether it will accept the data the draggable is carrying. The drag target will accept incoming drag if it belongs to the same `group` as draggable. If the user does drop the draggable on top of the drag target (and the drag target has indicated that it will accept the draggable's data), then the drag target is asked to accept the draggable's data."""

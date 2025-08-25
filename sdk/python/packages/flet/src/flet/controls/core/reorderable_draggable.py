from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.layout_control import LayoutControl


@control("ReorderableDraggable")
class ReorderableDraggable(LayoutControl, AdaptiveControl):
    """
    Used to drag an item in a [`ReorderableListView`][flet.ReorderableListView].

    It creates a listener for a drag immediately following a pointer down
    event over the given [`content`][(c).] control.

    Raises:
        AssertionError: If [`content`][(c).] is not visible.
    """

    index: int
    """
    The index of the associated item that will be dragged in the list.
    """

    content: Control
    """
    The control for which the application would like to respond to a tap and
    drag gesture by starting a reordering drag on a reorderable list.
    """

    def before_update(self):
        super().before_update()
        assert self.content.visible, "content must be visible"

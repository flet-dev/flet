---
class_name: flet.Dismissible
examples: ../../examples/controls/dismissible
---

{{ class_summary(class_name) }}

## Examples

### Dismissible `ListTile`s

{{ code_and_demo(examples + "/dismissible_list_tiles.py", demo_height="420", demo_width="100%") }}

### Remove Dismissible `on_dismiss` inside component

/// admonition | Important
    type: warning
Always specify a key for `Dismissible` when using inside Flet component.
///

The issue you may encounter here is specific to the `Dismissible` control used inside Flet component (declarative UI).

When a user swipes (dismisses) an item, that widget is marked as “dismissed” on the Flutter side and effectively removed from the UI.
However, when Flet recalculates the UI diff on the Python side, it may attempt to reuse widgets in the list based on their order rather than their identity.

If no key is provided, Flet’s diffing algorithm can’t tell that a particular `Dismissible` corresponds to a specific item — so it assumes the items have merely shifted.
That leads to update commands like:

> “Update text in items 0…N-1, then delete the last item (N).”

On Flutter’s side, though, the already-dismissed `Dismissible` widget in the middle of the list can’t be updated — it’s gone — causing runtime errors.

**Always assign a stable, unique key to each `Dismissible`, typically based on the item’s identifier or index.**

Example:

{{ code_and_demo(examples + "/remove_on_dismiss_declarative.py", demo_height="420", demo_width="100%") }}

{{ class_members(class_name) }}

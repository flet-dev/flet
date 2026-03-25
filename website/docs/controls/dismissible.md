---
class_name: "flet.Dismissible"
examples: "controls/dismissible"
example_images: "examples/controls/dismissible/media"
title: "Dismissible"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} />

## Examples

[Live example](https://flet-controls-gallery.fly.dev/layout/dismissible)

### Dismissible `ListTile`s

<CodeExample path={frontMatter.examples + '/dismissible_list_tiles.py'} language="python" />

<Image src={frontMatter.example_images + '/dismissible_list_tiles.gif'} alt="dismissible-list-tiles" width="55%" />

### Remove Dismissible `on_dismiss` inside component

:::warning[Important]
Always specify a key for `Dismissible` when using inside Flet component.
:::

The issue you may encounter here is specific to the `Dismissible` control used inside Flet component (declarative UI).

When a user swipes (dismisses) an item, that widget is marked as “dismissed” on the Flutter side and effectively removed from the UI.
However, when Flet recalculates the UI diff on the Python side, it may attempt to reuse widgets in the list based on their order rather than their identity.

If no key is provided, Flet’s diffing algorithm can’t tell that a particular `Dismissible` corresponds to a specific item — so it assumes the items have merely shifted.
That leads to update commands like:

> “Update text in items 0…N-1, then delete the last item (N).”

On Flutter’s side, though, the already-dismissed `Dismissible` widget in the middle of the list can’t be updated — it’s gone — causing runtime errors.

**Always assign a stable, unique key to each `Dismissible`, typically based on the item’s identifier or index.**

Example:

<CodeExample path={frontMatter.examples + '/remove_on_dismiss_declarative.py'} language="python" />

<ClassMembers name={frontMatter.class_name} />

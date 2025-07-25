Flet UI is built of "controls". These are organized into a hierarchy/tree,
in which each control has a parent (except [`Page`][flet.Page], the top-most control) and container controls
like [`Column`][flet.Column], [`Dropdown`][flet.Dropdown] can contain child controls, for example:

```
Page
 ├─ TextField
 ├─ Column
 │   ├─ Text
 │   └─ Image
 └─ Row
     ├─ Checkbox
     └─ ElevatedButton
```

The [control gallery](https://flet-controls-gallery.fly.dev/layout) provides a live demo of most of our controls.

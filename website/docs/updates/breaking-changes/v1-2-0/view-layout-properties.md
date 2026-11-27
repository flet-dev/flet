---
title: "View: layout properties are deprecated"
---

# `View`: layout properties are deprecated

:::note
This guide is accurate as of Flet 1.2.0. Later releases might add new APIs or
additional migration paths.

The [breaking changes and deprecations index](../index.md) lists the guides created for each release.
:::

## Summary

[`View`][flet.View] no longer inherits from [`LayoutControl`][flet.LayoutControl].
The properties it inherited from it never had an effect on a view, and are now
deprecated:

- size: `width`, `height`, `min_width`, `max_width`, `min_height`, `max_height`,
  `aspect_ratio`;
- position and alignment: `left`, `top`, `right`, `bottom`, `align`, `margin`;
- transforms: `rotate`, `scale`, `offset`, `flip`, `transform`;
- animations: `animate_opacity`, `animate_size`, `animate_position`,
  `animate_align`, `animate_margin`, `animate_rotation`, `animate_scale`,
  `animate_offset`, and `on_animation_end`.

Setting one of them logs a deprecation warning. Nothing else changes: they had no
effect before, and still don't.

[`View.on_size_change`][flet.View.on_size_change] and
[`View.size_change_interval`][flet.View.size_change_interval] stay. `on_size_change`
now fires, and reports the size of the view's body.

## Context

A view is a route: it always fills its page, the way the page fills the window. A
view can't be smaller than its page, or positioned, aligned, transformed or
animated within it, so none of these properties could apply.

## Migration guide

Remove these properties from your views.

To size, position, transform or animate a view's content, set them on a control
inside the view, such as a [`Container`][flet.Container] that holds the content:

```python
ft.View(
    route="/settings",
    controls=[
        ft.Container(
            content=settings_form,
            max_width=600,
            align=ft.Alignment.TOP_CENTER,
        )
    ],
)
```

For the size of the area a view's content can use, handle
[`View.on_size_change`][flet.View.on_size_change]. It reports the size of the
body: the area between the app bar and the bottom navigation bar or bottom app
bar. For the size of the whole page, handle
[`Page.on_resize`][flet.Page.on_resize].

## Timeline

- Deprecated in: `1.2.0`
- Removal in: `1.5.0`

## References

- Issue: [#6363](https://github.com/flet-dev/flet/issues/6363)
- Pull request: [#7088](https://github.com/flet-dev/flet/pull/7088)
- Docs: [`View`][flet.View], [`View.on_size_change`][flet.View.on_size_change]
- Release notes: [Flet 1.2.0](../../release-notes.md)

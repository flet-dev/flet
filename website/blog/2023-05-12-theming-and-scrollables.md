---
slug: scrolling-controls-and-theming
title: Scrolling controls and Theming
authors: feodor
tags: [releases]
---

Flet 0.7.1 enables developers [changing scroll position](#controlling-scroll-position) and [receiving scroll notifications](#receiving-scroll-notifications) from `Page`, `View`, `Column`, `Row`, `ListView` and `GridView` controls.

The release also introduces theming improvements:
* [Color scheme customization](#color-scheme-customization)
* [Nested themes](#nested-themes)
* [Text theming](#text-theming)
* [Scrollbar theming](#scrollbar-theme)
* [Tabs theming](#tabs-theming)

<!-- truncate -->

## Controlling scroll position

Scrollable controls (`Page`, `View`, `Column`, `Row`, `ListView` and `GridView`) introduce `scroll_to()` method to change their scroll position to either absolute `offset`, relative `delta` or jump to the control with specified `key`.

Moving to a `key` is particularly exciting as it allows simulating the navigation between page bookmarks, kind of HTML hrefs with `#`:

<img src="/img/docs/controls/column/column-scroll-to-key.gif"  className="screenshot-70 screenshot-rounded" />

Check the [source code](https://github.com/flet-dev/examples/blob/main/python/controls/column/column-scroll-to-key.py) of the example above.

See [`Column.scroll_to`](https://docs.flet.dev/controls/column/#flet.Column.scroll_to) for more details about controlling scroll position.

## Receiving scroll notifications

All scrollable controls now provide `on_scroll` event handler which fires when a scroll position is changed. From event object properties you can determine whether scroll operation has started, finished, changed direction or scroll position went behind scrolling extent (overscroll). You can also get updates of the current scroll position as well as dimensions of the scroll area, for example:

```python
import flet as ft

def main(page: ft.Page):
    def on_column_scroll(e: ft.OnScrollEvent):
        print(
            f"Type: {e.event_type}, pixels: {e.pixels}, min_scroll_extent: {e.min_scroll_extent}, max_scroll_extent: {e.max_scroll_extent}"
        )

    cl = ft.Column(
        spacing=10,
        height=200,
        width=200,
        scroll=ft.ScrollMode.ALWAYS,
        on_scroll=on_column_scroll,
    )
    for i in range(0, 50):
        cl.controls.append(ft.Text(f"Text line {i}", key=str(i)))

    page.add(
        ft.Container(cl, border=ft.border.all(1)),
    )

ft.run(main)
```

See [`Column.on_scroll`](https://docs.flet.dev/controls/column/#flet.Column.on_scroll) for more details about scroll notification.

Check [infinite scroll example](https://github.com/flet-dev/examples/blob/main/python/controls/column/column-infinite-list.py).

## Color scheme customization

Until today the only way to control color scheme for your application was specifying `color_scheme_seed` when creating a new `ft.Theme` object.

This release enables you to fine tune all 30 colors based on the [Material spec](https://m3.material.io/styles/color/the-color-system/color-roles) and used by various Flet controls.

<img src="/img/blog/theme-scrolling/material-theme-builder.png"  className="screenshot-70 screenshot-rounded" />

You can even use [Material Theme Builder](https://m3.material.io/theme-builder#/dynamic) and apply exported color palette to your app, for example:

```python
page.theme = ft.Theme(
    color_scheme=ft.ColorScheme(
        primary=ft.Colors.GREEN,
        primary_container=ft.Colors.GREEN_200
        # ...
    ),
)
```

See [`ColorScheme` class](https://docs.flet.dev/types/colorscheme/) for more details.

## Nested themes

Another awesome feature of this release is nested themes!

You can have a part of your app to use a different theme or override some theme styles for specific controls.

Remember `page` object having `theme` and `theme_mode` properties? Now `Container` has `theme` and `theme_mode` properties too!

`Container.theme` accepts the same `ft.Theme` object as a page. Specifying `theme_mode` in the container means you don't want to inherit parent theme, but want a completely new, unique scheme for all controls inside the container. However, if the container does not have `theme_mode` property set then the styles from its `theme` property will override the ones from the parent, inherited theme:

```python
import flet as ft

def main(page: ft.Page):
    # Yellow page theme with SYSTEM (default) mode
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.YELLOW,
    )

    page.add(
        # Page theme
        ft.Container(
            content=ft.ElevatedButton("Page theme button"),
            bgcolor=ft.Colors.SURFACE_VARIANT,
            padding=20,
            width=300,
        ),

        # Inherited theme with primary color overridden
        ft.Container(
            theme=ft.Theme(color_scheme=ft.ColorScheme(primary=ft.Colors.PINK)),
            content=ft.ElevatedButton("Inherited theme button"),
            bgcolor=ft.Colors.SURFACE_VARIANT,
            padding=20,
            width=300,
        ),

        # Unique always DARK theme
        ft.Container(
            theme=ft.Theme(color_scheme_seed=ft.Colors.INDIGO),
            theme_mode=ft.ThemeMode.DARK,
            content=ft.ElevatedButton("Unique theme button"),
            bgcolor=ft.Colors.SURFACE_VARIANT,
            padding=20,
            width=300,
        ),
    )

ft.run(main)
```

<img src="/img/blog/theme-scrolling/nested-themes.png"  className="screenshot-60" />

## Scrollbar theme

You can now customize the look and fill of scrollbars in your application (or a particular scroillbar with [nested themes](#nested-themes)).

It could be done via [`page.theme.scrollbar_theme`](https://docs.flet.dev/types/scrollbartheme/) property, for example:

```python
page.theme = ft.Theme(
    scrollbar_theme=ft.ScrollbarTheme(
        track_color={
            ft.MaterialState.HOVERED: ft.Colors.AMBER,
            ft.MaterialState.DEFAULT: ft.Colors.TRANSPARENT,
        },
        track_visibility=True,
        track_border_color=ft.Colors.BLUE,
        thumb_visibility=True,
        thumb_color={
            ft.MaterialState.HOVERED: ft.Colors.RED,
            ft.MaterialState.DEFAULT: ft.Colors.GREY_300,
        },
        thickness=30,
        radius=15,
        main_axis_margin=5,
        cross_axis_margin=10,
    )
)
```

<img src="/img/docs/controls/column/column-scroll-to.png"  className="screenshot-60" />

## Text theming

Material 3 design defines [5 groups of text styles with 3 sizes in each group](https://docs.flet.dev/controls/text/#pre-defined-theme-text-styles): "Display", "Headline", "Title", "Label" and "Body" which are used across Flet controls. You can now customize each of those styles with `page.theme.text_theme`, for example:

```python
import flet as ft

def main(page: ft.Page):
    page.theme = ft.Theme(
        text_theme=ft.TextTheme(body_medium=ft.TextStyle(color=ft.Colors.GREEN))
    )

    page.add(ft.Text("Hello, green world!"))

ft.run(main)
```

<img src="/img/blog/theme-scrolling/text-theme.png"  className="screenshot-50" />

Apparently, `Body Medium` is used by `Text` control as a default style.

See [`TextTheme` class](https://docs.flet.dev/types/texttheme/) for more details.

## Tabs theming

You can now control the look and feel of `Tabs` control. In this release `Tabs` adds a bunch of new properties and there is a new [`page.theme.tabs_theme`](https://docs.flet.dev/types/tabstheme/) property to style all tabs in your app:

```python
page.theme = ft.Theme(
    tabs_theme=ft.TabsTheme(
        divider_color=ft.Colors.BLUE,
        indicator_color=ft.Colors.RED,
        indicator_tab_size=True,
        label_color=ft.Colors.GREEN,
        unselected_label_color=ft.Colors.AMBER,
        overlay_color={
            ft.MaterialState.FOCUSED: ft.Colors.with_opacity(0.2, ft.Colors.GREEN),
            ft.MaterialState.DEFAULT: ft.Colors.with_opacity(0.2, ft.Colors.PINK),
        },
    )
)
```

<img src="/img/blog/theme-scrolling/tabs-theme.png"  className="screenshot-60" />

See [`TabsTheme` class](https://docs.flet.dev/types/tabstheme/) for more details.

## Other changes

### Flutter 3.10

This Flet release is based on Flutter 3.10 which [brings new features, performance and size optimizations](https://medium.com/flutter/whats-new-in-flutter-3-10-b21db2c38c73). As a result, most of Flet dependencies bumped their versions too, so if you notice any issues please let us know.

### Color emoji in web apps

Color emoji support in web apps are back! In Flutter 3.7 color emoji were disabled in "CanvasKit" renderer (default in Flet) because of their font size (8 MB!) and returned back as an opt-in in Flutter 3.10. You can enable color emoji in server-driven app with `use_color_emoji` argument:

```python
ft.run(main, use_color_emoji=True)
```

and [use `--use-color-emoji` switch](https://docs.flet.dev/publish/web/static-website/#color-emojis) when publishing app as a static side.

That's all for today!

Upgrade Flet module to the latest version (`pip install flet --upgrade`) and [let us know](https://discord.gg/dzWXP8SHG8) what you think!

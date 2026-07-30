---
title: "Creating a new Flet app"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';
import {CodeExample, Image} from '@site/src/components/crocodocs';

A Flet app's UI is made up of [controls](/docs/controls), arranged on the page. Controls can be styled, nested
inside each other to build layouts, and respond to events like clicks and taps.

This page walks through creating your first app, then the controls and events you'll use to build almost any UI,
tying them together into a small example app.

## Your first app

Create a new directory (or directory with `pyproject.toml` already exists if initialized with a project manager) and switch into it.

To create a new "minimal" Flet app run the following command:

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```bash
uv run flet create
```
</TabItem>
<TabItem value="pip" label="pip">
```bash
flet create
```
</TabItem>
</Tabs>
:::danger[Important]
Any existing `README.md` or `pyproject.toml` (for example, created by `uv init`)
will be replaced by the one created by [`flet create`](../cli/flet-create.md) command.
:::

The command will create the following directory structure:

```tree
README.md
pyproject.toml
src
    assets
        icon.png
        splash_android.png
    main.py # (1)!
tests
    test_main.py # (2)!
```

1. Contains a simple Flet program.
    It has `main()` function where you would add UI elements (controls) to a page or a window.
    The application ends with a `ft.run()` function which initializes the Flet app and [runs](running-app.md) `main()`.
2. A sample [integration test](integration-testing.md) for the app, ready to run with `flet test`.

You can find more information about `flet create` command [here](../cli/flet-create.md).

`src/main.py` already contains a small working counter app with a button that increments it:

<CodeExample path="apps/templates/basic_counter/main.py" language="python" title="src/main.py" />

<Image src="assets/getting-started/counter-app/macos.png" alt="Counter app running on macOS" width="60%" />

* [`page`](../controls/page.md) is the top-level container for everything in the app window (or browser tab).
* [`page.add()`](/docs/controls/basepage#flet.BasePage.add) appends controls to the page.
* [`page.floating_action_button`](../controls/floatingactionbutton.md) sets the round action button in the
  bottom-right corner.
* `increment_click` is an event handler (see [Handling events](#handling-events) below); Flet renders the changes
  it makes as soon as the handler returns.

See [Running a Flet app](running-app.md) to launch it as a desktop window or in a browser.

## Basic controls

You'll most likely need controls for showing text, laying out other controls, and adding a background, border, or
padding.

### Text

[`Text`](../controls/text.md) displays a string, with optional styling:

```python
ft.Text("Flet is fun to build with!", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE)
```

### Row and Column

[`Row`](../controls/row.md) and [`Column`](../controls/column.md) lay out their `controls` horizontally and
vertically, respectively. Both accept `alignment` (main axis) and `vertical_alignment`/`horizontal_alignment`
(cross axis) to control spacing and positioning:

```python
ft.Row(
    alignment=ft.MainAxisAlignment.CENTER,
    controls=[
        ft.Icon(ft.Icons.STAR),
        ft.Text("Featured"),
    ],
)
```

You can nest a `Column` inside a `Row` (or vice versa) to build more complex layouts.

### Stack

[`Stack`](../controls/stack.md) overlaps its children instead of laying them out in a line. Children are
positioned with `top`, `bottom`, `left`, and `right`, which makes `Stack` useful for badges, overlays, and anything
else that needs to sit on top of another control:

```python
ft.Stack(
    controls=[
        ft.CircleAvatar(foreground_image_src="https://picsum.photos/100"),
        ft.Container(
            width=14,
            height=14,
            bgcolor=ft.Colors.GREEN,
            border_radius=7,
            right=0,
            bottom=0,
        ),
    ],
)
```

### Container

[`Container`](../controls/container.md) wraps a single control and adds visual styling around it: background color,
border, border radius, padding, margin, and fixed width/height:

```python
ft.Container(
    content=ft.Text("Styled box"),
    bgcolor=ft.Colors.AMBER_100,
    padding=12,
    border_radius=8,
)
```

`Container` also accepts `on_click`, which makes it a handy way to make a control clickable when that control
doesn't have an `on_click` of its own: just wrap it in a `Container`. See [Handling events](#handling-events)
below.

## Structuring the page

Beyond individual controls, `page` itself has properties that shape the whole app: `page.title` sets the window/tab
title, and `page.appbar` puts an [`AppBar`](../controls/appbar.md) (the header row with a title and actions) at
the top of the page:

```python
def main(page: ft.Page):
    page.title = "My App"
    page.appbar = ft.AppBar(
        title=ft.Text("My App"),
        bgcolor=ft.Colors.SURFACE_TINT,
        actions=[ft.IconButton(ft.Icons.SETTINGS)],
    )
    page.add(ft.Text("Body content goes here"))

ft.run(main)
```

`page.theme` and `page.theme_mode` control the color scheme (light/dark and a seed color) applied across all
Material controls on the page (see [Theming](../cookbook/theming.md) for more).

:::note[Note]
`AppBar`, `Button`, and most other controls follow Material Design. For an iOS-style look, Flet also ships a
parallel set of Cupertino controls (`ft.Cupertino*`). See [Adaptive apps](../cookbook/adaptive-apps.md) for
building a single app that looks native on both platforms.
:::

## Handling events

Interactive controls like [`Button`](../controls/button.md), [`IconButton`](../controls/iconbutton.md), and
[`Container`](../controls/container.md) accept event handlers, plain functions that run when the user interacts
with the control:

```python
def main(page: ft.Page):
    def handle_click(e: ft.Event[ft.Button]):
        page.show_dialog(ft.SnackBar(ft.Text("Button clicked!")))

    page.add(ft.Button("Click me", on_click=handle_click))

ft.run(main)
```

Every event handler takes a single argument, conventionally named `e`, of type [`Event`](/docs/types/event).
`e.control` is the control that triggered the event, so you can read its current state from there (a `TextField`'s
`on_change` handler, for example, reads the new value via `e.control.value`). Typing the handler as
`ft.Event[ft.Button]`, as above, tells your editor that `e.control` is specifically a `Button`.

Anything you change inside a handler (a control property, or, as above, calling a page method like
`show_dialog()`) is picked up [automatically](../cookbook/auto-update.md), so most handlers don't need to manage
updates by hand.

For lower-level pointer interactions (taps, drags, hover, scroll), wrap a control in
[`GestureDetector`](../controls/gesturedetector.md).

## Example: Product catalog

Here's a small product catalog that uses everything above: an `AppBar` for the page header, `Container` and
`Column`/`Row` for layout and styling, a `Stack` to draw a "Sale" badge on one item, and `on_click` handlers to
react to taps:

<CodeExample path="cookbook/create_flet_app/product_catalog/main.py" language="python" title="catalog.py" />

<Image src="test-images/examples/cookbook/golden/macos/product_catalog/product_catalog.png"
       alt="Product catalog app running on macOS" width="60%" />

Run it with [`flet run`](running-app.md) and you'll get a scrollable list of product cards, each with a "Buy"
button that pops up a confirmation.

## What's next

* [Running a Flet app](running-app.md): see the apps above running as a desktop window or in a browser.
* [Controls reference](/docs/controls): the full list of controls available in Flet.
* [Auto-update](../cookbook/auto-update.md): how and when Flet sends control changes to the client.
* [Declarative vs. imperative](../cookbook/declarative-vs-imperative.md): once your UI needs to manage evolving
  state (like a shopping cart or a to-do list), this is the next thing to read.
* [Theming](../cookbook/theming.md): customize colors, fonts, and light/dark mode across the app.

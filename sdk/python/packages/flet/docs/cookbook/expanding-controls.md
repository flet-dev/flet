---
title: Expanding Controls
examples: ../../examples/apps/expand
example_images: ../test-images/examples/apps/golden/macos/expand
---

## `expand`

When a child control is placed into a [`Row`][flet.Row], [`Column`][flet.Column], [`View`][flet.View]
or [`Page`][flet.Page] you can "expand" it to fill the available space.

When adding child controls to a [`Row`][flet.Row], you can make them automatically
grow to fill available horizontal space using the [`expand`][flet.Control.expand] property,
which all Flet controls (inheriting from [`Control`][flet.Control]) have.

It lets you control how they use free space inside a
layout like [`Row`][flet.Row] or [`Column`][flet.Column].

You can set `expand` to one of the following values:

* a boolean — Whether the control should take all the available space.
* an integer — Used to proportionally divide free space among multiple expanding controls (useful when you want more control over sizing).

### Example 1

In this example, a [`TextField`][flet.TextField] stretches to fill all remaining space in the row,
while the [`Button`][flet.Button] stays sized to its content:

```python
--8<-- "{{ examples }}/expand_example_1.py"
```

{{ image(example_images + "/expand_example_1.png", alt="expand example 1", width="70%") }}

### Example 2

In this example, we create a [`Row`][flet.Row] with three [`Container`][flet.Container]s, distributed like 20% / 60% / 20%:

```python
--8<-- "{{ examples }}/expand_example_2.py"
```

Here, the available space is split into 5 total parts (1+3+1).
The first and third containers get 1 part each (20%), and the middle one gets 3 parts (60%).

{{ image(example_images + "/expand_example_2.png", alt="expand example 2", width="70%") }}

### Example 3

This example demonstrates how two controls inside a [`Row`][flet.Row] can
each expand to fill half of the available horizontal space using expand=True.

The layout uses a parent [`Container`][flet.Container] and a nested row, where both controls are
expanded equally, resulting in a 50/50 split.

```python
--8<-- "{{ examples }}/expand_example_3.py"
```

{{ image(example_images + "/expand_example_3.png", alt="expand example 3", width="70%") }}

## `expand_loose`

The [`expand_loose`][flet.Control.expand_loose] property allows a control to *optionally* expand
and fill the available space along the main axis of its parent container
(e.g., horizontally in a [`Row`][flet.Row], or vertically in a [`Column`][flet.Column]).

Unlike [`expand`][flet.Control.expand], which *forces* the control to occupy all available space,
`expand_loose` gives the control **flexibility** to grow **if needed**, but it’s not required to fill the space.

/// admonition | Note
For this property to have effect:

- it must be used on child controls within the following layout containers,
or any of their subclasses: [`Row`][flet.Row], [`Column`][flet.Column], [`View`][flet.View], [`Page`][flet.Page]
- the control using this property must have a non-none value for [`expand`][flet.Control.expand].
///

### Example 1

In this example, [`Container`][flet.Container]s being placed in [`Row`][flet.Row]s with `expand_loose = True`:

```python
--8<-- "{{ examples }}/expand_loose_example_1.py"
```

{{ image("../assets/controls/control/expand-loose.png", alt="expand_loose", width="65%") }}

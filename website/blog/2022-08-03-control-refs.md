---
slug: control-refs
title: Control Refs
authors: feodor
tags: [how-to]
---

Flet controls are objects and to access their properties we need to keep references (variables) to those objects.

Consider the following example:

```python {6-8,18,19,21}
import flet as ft

def main(page):

    first_name = ft.TextField(label="First name", autofocus=True)
    last_name = ft.TextField(label="Last name")
    greetings = ft.Column()

    def btn_click(e):
        greetings.controls.append(ft.Text(f"Hello, {first_name.value} {last_name.value}!"))
        first_name.value = ""
        last_name.value = ""
        page.update()
        first_name.focus()

    page.add(
        first_name,
        last_name,
        ft.ElevatedButton("Say hello!", on_click=btn_click),
        greetings,
    )

ft.run(main)
```

In the very beginning of `main()` method we create three controls which we are going to use in button's `on_click` handler: two `TextField` for first and last names and a `Column` - container for greeting messages. We create controls with all their properties set and in the end of `main()` method, in `page.add()` call, we use their references (variables).

When more and mode controls and event handlers added it becomes challenging to keep all control definitions in one place, so they become scattered across `main()` body. Glancing at `page.add()` parameters it's hard to imagine (without constant jumping to variable definitions in IDE) what would the end form look like:

```python {2-5}
    page.add(
        first_name,
        last_name,
        ft.ElevatedButton("Say hello!", on_click=btn_click),
        greetings,
    )
```

Is `first_name` a TextField, does it have autofocus set? Is greetings a `Row` or a `Column`?

<!-- truncate -->

## `Ref` class

Flet provides `Ref` utility class which allows to define a reference to the control, use that reference in event handlers and set the reference to a real control later, while building a tree. The idea comes from [React](https://reactjs.org/docs/refs-and-the-dom.html).

To define a new typed control reference:

```python
first_name = ft.Ref[ft.TextField]()
```

To access referenced control (control de-reference) use `Ref.current` property:

```python
# empty first name
first_name.current.value = ""
```

To assign control to a reference set `Control.ref` property to a reference:

```python {2}
page.add(
    ft.TextField(ref=first_name, label="First name", autofocus=True)
)
```

:::note
All Flet controls have `ref` property.
:::

We could re-write our program to use references:

```python {7-9,21-24}
import flet as ft


def main(page):

    first_name = ft.Ref[ft.TextField]()
    last_name = ft.Ref[ft.TextField]()
    greetings = ft.Ref[ft.Column]()

    def btn_click(e):
        greetings.current.controls.append(
            ft.Text(f"Hello, {first_name.current.value} {last_name.current.value}!")
        )
        first_name.current.value = ""
        last_name.current.value = ""
        page.update()
        first_name.current.focus()

    page.add(
        ft.TextField(ref=first_name, label="First name", autofocus=True),
        ft.TextField(ref=last_name, label="Last name"),
        ft.ElevatedButton("Say hello!", on_click=btn_click),
        ft.Column(ref=greetings),
    )

ft.run(main)
```

Now we can clearly see in `page.add()` the structure of the page and all the controls it's built of.

Yes, the logic becomes a little bit more verbose as you need to add `.current.` to access ref's control, but it's a matter of personal preference :)

[Give Flet a try](https://docs.flet.dev/) and [let us know](https://discord.gg/dzWXP8SHG8) what you think!
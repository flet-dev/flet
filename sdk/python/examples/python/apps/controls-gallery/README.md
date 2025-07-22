# Flet Controls Gallery app

Flet Controls Gallery app showcases examples of Flet controls usage.

# How to contribute

Contributions are welcome!

Fork this repo.

Install Python SDK as described [here](https://github.com/flet-dev/flet/blob/main/CONTRIBUTING.md#python-sdk).

## To add a new Control to an existing Control Group:
1. Create a new folder within the Control Group folder with the name of the Control
2. Create index.py file with the following contents:

```
name = "<Control name>"
description = """<Control description>"""
```

## To add a new example to an existing Control:
1. Create file named `XX_example_name.py`, where XX would be the order number of an example to be displayed for this control, starting with 01, for example "01_expansiontile_example.py", with the following contents:

```
import flet as ft

name = "<Example name>"

def example():
    return ft.Text("This example is under construction")
```

2. Replace `Text` control with the control you want to display.

Note: Controls Gallery is an [async app](https://flet.dev/docs/guides/python/async-apps). If an event handler calls any async methods such as `update_async`, it should be `async` as well.

Submit Pull Request (PR) with your changes.

When the contribution is tested by Flet team/community a new Flet Controls Gallery release will be published.

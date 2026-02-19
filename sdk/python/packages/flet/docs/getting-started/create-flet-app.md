Create a new directory (or directory with `pyproject.toml` already exists if initialized with a project manager) and switch into it.

To create a new "minimal" Flet app run the following command:

/// tab | uv
```bash
uv run flet create
```
///
/// tab | pip
```bash
flet create
```
///

/// admonition | Important
    type: danger
Any existing `README.md` or `pyproject.toml` (for example, created by `uv init`)
will be replaced by the one created by [`flet create`](../cli/flet-create.md) command.
///

The command will create the following directory structure:

```tree
README.md
pyproject.toml
src
    assets
        icon.png
    main.py # (1)!
storage
    data
    temp
```

1. Contains a simple Flet program.
    It has `main()` function where you would add UI elements (controls) to a page or a window.
    The application ends with a `ft.run()` function which initializes the Flet app and [runs](running-app.md) `main()`.

You can find more information about `flet create` command [here](../cli/flet-create.md).

**Now let's see Flet in action by [running the app](running-app.md)!**

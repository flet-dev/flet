Create a new directory (or directory with `pyproject.toml` already exists if initialized with `poetry` or `uv`) and switch into it.

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
/// tab | poetry
```bash
poetry run flet create
```
///

/// admonition 
    type: note
Any existing `README.md` or `pyproject.toml` (for example, created by `uv init` or `poetry init`) 
will be replaced by the one created by `flet create` command.
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
    It has `main()` function where you would add UI elements ([controls](flet-controls)) to a page or a window. 
    The application ends with a `ft.run()` function which initializes the Flet app and [runs](running-app.md) `main()`.

You can find more information about `flet create` command [here](TBA).

Now let's see Flet in action by [running the app](running-app.md)!

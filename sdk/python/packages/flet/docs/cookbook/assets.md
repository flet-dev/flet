Flet apps can include both code and assets/resources.
An asset is a file that is bundled and deployed with your app and is accessible at runtime.
Common types of assets include static data (e.g., JSON files), configuration files, icons, images, videos, etc.

To use relative paths for your asset files, you need to provide a path to your assets directory
when launching your app with the `ft.run()` function.
The parameter for this is called `assets_dir`, which defaults to `"assets"`.
This parameter specifies the folder where local assets are stored and can be either an absolute
path or a path relative to the app's entry point file, such as `main.py`.

## Example: Displaying a Local Image

Suppose you have a folder named `assets` in the same directory as your `main.py` file, and
this folder contains an image file named `sample.png` in a subfolder called `images`:

```tree
assets
    images
        sample.png
main.py
```

To display this image in your app, you can do the following:

```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.Image(src="images/sample.png")
    )

ft.run(main, assets_dir="assets")
```

The same approach applies to other asset types like fonts, Lottie animations, Rive files, etc.

## Accessing Asset Files in Production

For UI controls such as [`Image`][flet.Image], you usually pass a path relative to `assets_dir`:

```python
ft.Image(src="images/sample.png")
```

For non-UI file operations (ex: reading JSON, opening a bundled SQLite database, loading ML models, etc.),
it is often more convenient to use an absolute path to your assets directory.
For this reason, Flet sets the [`FLET_ASSETS_DIR`](../reference/environment-variables.md#flet_assets_dir)
environment variable (in production apps built with [`flet build`](../publish/index.md),excluding `web`)
to an absolute path to your assets directory.

You can use it with a local-development fallback, as shown in the below example (which assumes the asset folder is named `"assets"`):

```python
import json
import os
from pathlib import Path

import flet as ft


def get_assets_dir() -> Path:
    default_assets_dir = Path(__file__).parent / "assets"   # fallback for local runs
    return Path(os.environ.get("FLET_ASSETS_DIR", str(default_assets_dir))).resolve()


def main(page: ft.Page):
    assets_dir = get_assets_dir()

    # load a JSON file
    with (assets_dir / "data" / "some_config.json").open() as f:
        config = json.load(f)

    page.add(ft.Text(f"Loaded profile: {config['profile_name']}"))


ft.run(main, assets_dir="assets")
```

This gives you a single way to resolve bundled files across local runs and production builds.
See [`FLET_ASSETS_DIR`](../reference/environment-variables.md#flet_assets_dir) for details.

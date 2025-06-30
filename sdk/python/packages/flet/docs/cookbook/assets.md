---
title: Assets
sidebar_label: Assets
---

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
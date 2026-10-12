# Flet platform assets

[![python](https://img.shields.io/badge/python-%3E%3D3.10-%2334D058)](https://pypi.org/project/flet-platform-assets)
[![docstring coverage](https://flet.dev/docs/assets/badges/docs-coverage/flet-platform-assets.svg)](https://flet.dev/docs/assets/badges/docs-coverage/flet-platform-assets.svg)

Turns one source image into every app icon and splash screen a platform expects —
iOS and macOS asset catalogs, Android mipmaps and adaptive layers, a multi-size
Windows `.ico`, the Linux hicolor tree, and web favicons, maskable icons and
splash images.

> **[Try Flet online in Flet Studio](https://studio.flet.dev)**
>
> Start your next Flet app in the browser, then use this package locally to prepare its icons and splash screens. Write your own Python code or get help from the AI agent.

Used by `flet build`, and importable on its own. Pillow handles raster images and
`resvg_py` renders SVG; neither requires a separately installed conversion tool.
Nothing here imports `flet` or `flet-cli`.

## Rendering is separate from writing

`render_*()` is pure: it takes images and returns images, never touching the
filesystem and never printing. That makes it usable behind a UI that previews
icons before anything is built.

```python
from flet_platform_assets import IconOptions, load_source, render_icons, write

source, _ = load_source("assets/icon.svg")
result = render_icons(source, IconOptions())

for asset in result.assets:          # preview
    print(asset.relative_path, asset.image.size, asset.image.mode)
for warning in result.warnings:      # diagnostics are data, not log output
    print(warning)

write(result, "build/flutter")       # the only step that touches disk
```

SVG sources are rendered in memory to fit within 2048 × 2048 pixels, keeping
their aspect ratio and transparency. A square `viewBox`, such as `0 0 24 24`,
works at every output size; no intermediate PNG is written to your assets.
Use self-contained SVGs with vector paths and embedded images. Convert text to
paths to keep the result independent of fonts installed on the build host.

`load_source(path, svg_size=1024)` uses a smaller SVG render canvas. `flet build`
uses this for splashes, matching the on-screen size of a 1024px PNG source.

## What it will not do

It never re-frames your artwork. The padding inside your icon is a design
decision, so only transforms the platform actually requires are applied —
flattening where alpha is rejected, the macOS icon grid, multi-size `.ico`,
opaque maskable icons.

The one exception is the Android 12 splash icon, whose canvas is a platform
frame with a guaranteed-cropped outer third; there the artwork is fitted to the
visible circle rather than silently clipped.

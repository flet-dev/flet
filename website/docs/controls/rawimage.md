---
class_name: "flet.RawImage"
examples: "controls/core/raw_image"
example_images: "test-images/examples/controls/core/golden/macos/raw_image"
title: "RawImage"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="RawImage" imageWidth="30%" />

## `RawImage` vs `Image`

Use [`Image`](/docs/controls/image) for pictures that come from a file, URL,
asset or a one-off byte string. Use `RawImage` when your Python code *produces*
pixels — Pillow drawings, NumPy arrays, camera frames, plots, procedural
animations — and you want to push them to the screen repeatedly and fast.

Every update of `Image.src` travels through the regular Flet protocol and is
decoded from scratch on the client. `RawImage` instead streams frames over a
dedicated data channel: bytes skip the protocol entirely and, when the client
runs on the same machine (desktop app, `flet run`, Pyodide), frames are
transferred as raw RGBA pixels and uploaded straight to a GPU texture — no
image encoding or decoding on either side. Remote web clients automatically
receive compact PNG frames instead.

The `render` methods are awaitable and resolve when the client has displayed
the frame, so a plain loop self-paces to display speed:

```python
raw_image = ft.RawImage(expand=True)
page.add(raw_image)

while True:
    await raw_image.render(produce_pil_image())
```

## Examples

### Photo viewer

Regular PNG/JPEG/WebP bytes — downloaded, read from a file or pulled from a
database — are displayed with `render_encoded`; the client decodes them with
its image codecs.

<CodeExample path={frontMatter.examples + '/photo_viewer/main.py'} language="python" />

### Plasma animation

Streams a procedurally generated plasma effect with a live FPS counter and a
render-resolution slider.

<CodeExample path={frontMatter.examples + '/plasma/main.py'} language="python" />

### Pillow paint

An interactive paint app: pan gestures draw brush strokes onto a Pillow image
that is streamed to the screen through a dirty-flag render loop.

<CodeExample path={frontMatter.examples + '/paint/main.py'} language="python" />

### Mandelbrot explorer

Click to zoom into the Mandelbrot set — every zoom is a burst of NumPy-rendered
frames computed in a background thread.

<CodeExample path={frontMatter.examples + '/mandelbrot/main.py'} language="python" />

### Game of Life

Conway's Game of Life on a tiny grid upscaled with crisp nearest-neighbor
filtering; draw cells with the pointer while the simulation runs.

<CodeExample path={frontMatter.examples + '/game_of_life/main.py'} language="python" />

<ClassMembers name={frontMatter.class_name} />

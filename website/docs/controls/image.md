---
class_name: "flet.Image"
examples: "controls/image"
example_images: "test-images/examples/core/golden/macos/image"
example_media: "examples/controls/image/media"
title: "Image"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Basic Image" />

## Examples

[Live example](https://flet-controls-gallery.fly.dev/displays/image)

### Image gallery

<CodeExample path={frontMatter.examples + '/gallery.py'} language="python" />

<Image src={frontMatter.example_media + '/gallery.gif'} width="55%" />

### Fade-in images with a placeholder

<CodeExample path={frontMatter.examples + '/fade_in.py'} language="python" />

### Displaying images from base64 strings and byte data

<CodeExample path={frontMatter.examples + '/src_base64_and_bytes.py'} language="python" />

### Displaying a static SVG image

<CodeExample path={frontMatter.examples + '/static_svg.py'} language="python" />

### Displaying a dynamic SVG image

<CodeExample path={frontMatter.examples + '/dynamic_svg.py'} language="python" />

### Displaying a Lucide icon

<CodeExample path={frontMatter.examples + '/lucide_icons.py'} language="python" />

### Gapless playback when changing image sources

This example updates both images to a new network URL on each click. With
[`gapless_playback`](image.md#flet.Image-gapless_playback) set to `True`, the previous frame remains visible while the next
image loads. With [`gapless_playback`](image.md#flet.Image-gapless_playback) set to `False`, the image area can
briefly be empty, causing a flicker/blink effect.

<CodeExample path={frontMatter.examples + '/gapless_playback.py'} language="python" />

<ClassMembers name={frontMatter.class_name} />

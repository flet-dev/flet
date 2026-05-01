---
class_name: "flet.Image"
examples: "controls/core/image"
example_images: "test-images/examples/controls/core/golden/macos/image"
example_media: "examples/controls/core/image/media"
title: "Image"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Basic Image" imageWidth="10%" />

## Examples

[Live example](https://flet-controls-gallery.fly.dev/displays/image)

### Image gallery

<CodeExample path={frontMatter.examples + '/gallery/main.py'} language="python" />

<Image src={frontMatter.example_media + '/gallery.gif'} width="45%" />

### Fade-in images with a placeholder

<CodeExample path={frontMatter.examples + '/fade_in/main.py'} language="python" />

### Displaying images from base64 strings and byte data

<CodeExample path={frontMatter.examples + '/src_base64_and_bytes/main.py'} language="python" />

### Displaying a static SVG image

<CodeExample path={frontMatter.examples + '/static_svg/main.py'} language="python" />

### Displaying a dynamic SVG image

<CodeExample path={frontMatter.examples + '/dynamic_svg/main.py'} language="python" />

### Displaying a Lucide icon

<CodeExample path={frontMatter.examples + '/lucide_icons/main.py'} language="python" />

### Gapless playback when changing image sources

This example updates both images to a new network URL on each click. With
[`gapless_playback`](image.md#flet.Image.gapless_playback) set to `True`, the previous frame remains visible while the next
image loads. With [`gapless_playback`](image.md#flet.Image.gapless_playback) set to `False`, the image area can
briefly be empty, causing a flicker/blink effect.

<CodeExample path={frontMatter.examples + '/gapless_playback/main.py'} language="python" />

<ClassMembers name={frontMatter.class_name} />

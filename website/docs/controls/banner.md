---
class_name: "flet.Banner"
examples: "controls/banner"
example_images: "test-images/examples/material/golden/macos/banner"
example_media: "examples/controls/banner/media"
title: "Banner"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Basic Banner" />

## Examples

[Live example](https://flet-controls-gallery.fly.dev/dialogs/banner)

### Basic example

<CodeExample path={frontMatter.examples + '/basic/main.py'} language="python" />

<Image src={frontMatter.example_media + '/basic.gif'} alt="basic" width="50%" />

<ClassMembers name={frontMatter.class_name} />

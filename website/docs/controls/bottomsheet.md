---
class_name: "flet.BottomSheet"
examples: "controls/bottom_sheet"
example_images: "test-images/examples/material/golden/macos/bottom_sheet"
title: "BottomSheet"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Basic BottomSheet" />

## Examples

[Live example](https://flet-controls-gallery.fly.dev/dialogs/bottomsheet)

### Basic example

<CodeExample path={frontMatter.examples + '/basic/main.py'} language="python" />

<Image src={frontMatter.example_images + '/basic.gif'} width="40%" />

### Fullscreen

<CodeExample path={frontMatter.examples + '/fullscreen/main.py'} language="python" />

<Image src={frontMatter.example_images + '/fullscreen.gif'} width="40%" />

<ClassMembers name={frontMatter.class_name} />

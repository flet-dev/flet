---
class_name: "flet.Switch"
examples: "controls/switch"
example_images: "test-images/examples/material/golden/macos/switch"
example_media: "examples/controls/switch/media"
title: "Switch"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Basic switch and disabled switch" />

## Examples

[Live example](https://flet-controls-gallery.fly.dev/input/switch)

### Basic Example

<CodeExample path={frontMatter.examples + '/basic.py'} language="python" />

<Image src={frontMatter.example_images + '/basic.png'} alt="basic" width="55%" />

### Handling change events

<CodeExample path={frontMatter.examples + '/handling_events.py'} language="python" />

<Image src={frontMatter.example_media + '/handling_events.gif'} alt="handling-events" width="55%" />

<ClassMembers name={frontMatter.class_name} />

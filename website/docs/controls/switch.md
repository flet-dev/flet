---
class_name: "flet.Switch"
examples: "controls/material/switch"
example_images: "test-images/examples/material/golden/macos/switch"
example_media: "examples/controls/material/switch/media"
title: "Switch"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Basic switch and disabled switch" imageWidth="20%"/>

## Examples

[Live example](https://flet-controls-gallery.fly.dev/input/switch)

### Basic Example

<CodeExample path={frontMatter.examples + '/basic/main.py'} language="python" />

<Image src={frontMatter.example_images + '/basic.png'} alt="basic" width="40%" />

### Handling change events

<CodeExample path={frontMatter.examples + '/handling_events/main.py'} language="python" />

<Image src={frontMatter.example_media + '/handling_events.gif'} alt="handling-events" width="40%" />

<ClassMembers name={frontMatter.class_name} />

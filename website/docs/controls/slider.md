---
class_name: "flet.Slider"
examples: "../../examples/controls/slider"
example_images: "../test-images/examples/material/golden/macos/slider"
title: "Slider"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Basic slider" />

## Examples

[Live example](https://flet-controls-gallery.fly.dev/input/slider/basic)

### Basic Example

<CodeExample path={frontMatter.examples + '/basic.py'} />

<Image src={frontMatter.example_images + '/basic.png'} alt="basic" width="55%" />

### Setting a custom label

<CodeExample path={frontMatter.examples + '/custom_label.py'} />

<Image src={frontMatter.example_images + '/custom_label.png'} alt="custom-label" width="55%" />

### Handling events

<CodeExample path={frontMatter.examples + '/handling_events.py'} />

<Image src={frontMatter.example_images + '/handling_events.png'} alt="handling-events" width="55%" />

<ClassMembers name={frontMatter.class_name} />

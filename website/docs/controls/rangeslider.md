---
class_name: "flet.RangeSlider"
examples: "controls/range_slider"
example_images: "test-images/examples/material/golden/macos/range_slider"
title: "RangeSlider"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Range Slider" />

## Examples

[Live example](https://flet-controls-gallery.fly.dev/input/rangeslider)

### Basic Example

<CodeExample path={frontMatter.examples + '/basic/main.py'} language="python" />

<Image src={frontMatter.example_images + '/basic.gif'} alt="basic" width="55%" />

### RangeSlider with events

<CodeExample path={frontMatter.examples + '/handling_change_events/main.py'} language="python" />

<Image src={frontMatter.example_images + '/handling_events.gif'} alt="handling_events" width="55%" />

<ClassMembers name={frontMatter.class_name} />

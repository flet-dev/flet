---
class_name: "flet.TimePicker"
examples: "controls/time_picker"
example_images: "test-images/examples/material/golden/macos/time_picker"
title: "TimePicker"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Time picker" />

## Examples

[Live example](https://flet-controls-gallery.fly.dev/dialogs/timepicker)

### Basic Example

<CodeExample path={frontMatter.examples + '/basic/main.py'} language="python" />

<Image src={frontMatter.example_images + '/basic.png'} width="55%" />

### Hour Formats

<CodeExample path={frontMatter.examples + '/hour_formats/main.py'} language="python" />

<Image src={frontMatter.example_images + '/hour_formats.gif'} width="55%" />

<ClassMembers name={frontMatter.class_name} />

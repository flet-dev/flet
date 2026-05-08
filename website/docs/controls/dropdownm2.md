---
class_name: "flet.DropdownM2"
examples: "controls/material/dropdown_m2"
example_images: "test-images/examples/controls/material/golden/macos/dropdown_m2"
example_media: "examples/controls/material/dropdown_m2/media"
title: "DropdownM2"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Basic DropdownM2" imageWidth="25%"/>

## Examples

[Live example](https://flet-controls-gallery.fly.dev/input/dropdown)

### Basic Example

<CodeExample path={frontMatter.examples + '/basic/main.py'} language="python" />

<Image src={frontMatter.example_media + '/basic.gif'} alt="basic" width="40%" />

### Dropdown with label and hint

<CodeExample path={frontMatter.examples + '/label_and_hint/main.py'} language="python" />

<Image src={frontMatter.example_media + '/label_and_hint.gif'} alt="label-and-hint" width="35%" />

### Handling events

<CodeExample path={frontMatter.examples + '/handling_events/main.py'} language="python" />

<Image src={frontMatter.example_media + '/handling_events.gif'} alt="handling-events" width="40%" />

### Add and delete options

<CodeExample path={frontMatter.examples + '/add_and_delete_options/main.py'} language="python" />

<Image src={frontMatter.example_media + '/add_and_delete_options.gif'} alt="add-and-delete-options" width="50%" />

<ClassMembers name={frontMatter.class_name} />

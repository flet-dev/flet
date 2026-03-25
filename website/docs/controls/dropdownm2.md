---
class_name: "flet.DropdownM2"
examples: "controls/dropdown_m2"
example_images: "../test-images/examples/material/golden/macos/dropdown_m2"
example_media: "../examples/controls/dropdown_m2/media"
title: "DropdownM2"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Basic DropdownM2" />

## Examples

[Live example](https://flet-controls-gallery.fly.dev/input/dropdown)

### Basic Example

<CodeExample path={frontMatter.examples + '/basic.py'} language="python" />

<Image src={frontMatter.example_media + '/basic.gif'} alt="basic" width="55%" />

### Dropdown with label and hint

<CodeExample path={frontMatter.examples + '/label_and_hint.py'} language="python" />

<Image src={frontMatter.example_media + '/label_and_hint.gif'} alt="label-and-hint" width="55%" />

### Handling events

<CodeExample path={frontMatter.examples + '/handling_events.py'} language="python" />

<Image src={frontMatter.example_media + '/handling_events.gif'} alt="handling-events" width="55%" />

### Add and delete options

<CodeExample path={frontMatter.examples + '/add_and_delete_options.py'} language="python" />

<Image src={frontMatter.example_media + '/add_and_delete_options.gif'} alt="add-and-delete-options" width="55%" />

<ClassMembers name={frontMatter.class_name} />

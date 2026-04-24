---
class_name: "flet.Chip"
examples: "controls/material/chip"
example_images: "test-images/examples/controls/material/golden/macos/chip"
example_media: "examples/controls/material/chip/media"
title: "Chip"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Basic Chip" imageWidth="20%"/>

## Examples

[Live example](https://flet-controls-gallery.fly.dev/input/chip)

### Assist chips

Assist chips are chips with [`leading`](chip.md#flet.Chip.leading) icon
and [`on_click`](chip.md#flet.Chip.on_click) event specified.

They represent smart or automated actions that appear dynamically and contextually in a UI.

An alternative to assist chips are buttons, which should appear persistently and consistently.

<CodeExample path={frontMatter.examples + '/assist_chips/main.py'} language="python" />

<Image src={frontMatter.example_images + '/assist_chips.png'} alt="assist-chips" width="50%" />

### Filter chips

Filter chips are chips with [`on_select`](chip.md#flet.Chip.on_select) event specified.

They use tags or descriptive words provided in the [`label`](chip.md#flet.Chip.label) to filter content.
They can be a good alternative to switches or checkboxes.

<CodeExample path={frontMatter.examples + '/filter_chips/main.py'} language="python" />

<Image src={frontMatter.example_images + '/filter_chips.png'} alt="filter-chips" width="80%" />

<ClassMembers name={frontMatter.class_name} />

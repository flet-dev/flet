---
class_name: "flet.TextField"
examples: "../../examples/controls/text_field"
example_images: "../test-images/examples/material/golden/macos/textfield"
example_media: "../examples/controls/text_field/media"
title: "TextField"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Basic TextField" />

## Examples

[Live example](https://flet-controls-gallery.fly.dev/input/textfield)

### Basic Example

<CodeExample path={frontMatter.examples + '/basic.py'} />

<Image src={frontMatter.example_media + '/basic.gif'} alt="basic" width="55%" />

### Handling change events

<CodeExample path={frontMatter.examples + '/handling_change_events.py'} />

<Image src={frontMatter.example_media + '/handling_change_events.gif'} alt="handling-change-events" width="55%" />

### Handling selection changes

<CodeExample path={frontMatter.examples + '/selection_change.py'} />

### Password with reveal button

<CodeExample path={frontMatter.examples + '/password.py'} />

<Image src={frontMatter.example_media + '/password.gif'} alt="password" width="55%" />

### Multiline fields

<CodeExample path={frontMatter.examples + '/multiline.py'} />

<Image src={frontMatter.example_media + '/multiline.gif'} alt="multiline" width="55%" />

### Underlined and borderless TextFields

<CodeExample path={frontMatter.examples + '/underlined_and_borderless.py'} />

<Image src={frontMatter.example_media + '/underlined_and_borderless.gif'} alt="underlined-and-borderless" width="55%" />

### Setting prefixes and suffixes

<CodeExample path={frontMatter.examples + '/prefix_and_suffix.py'} />

<Image src={frontMatter.example_media + '/prefix_and_suffix.gif'} alt="prefix-and-suffix" width="55%" />

### Styled TextField

<CodeExample path={frontMatter.examples + '/styled.py'} />

### Custom label, hint, helper, and counter texts and styles

<CodeExample path={frontMatter.examples + '/label_hint_helper_counter.py'} />

<ClassMembers name={frontMatter.class_name} />

---
class_name: "flet.Checkbox"
examples: "controls/checkbox"
example_images: "test-images/examples/material/golden/macos/checkbox"
title: "Checkbox"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Basic checkboxes" />

## Examples

[Live example](https://flet-controls-gallery.fly.dev/input/checkbox)

### Basic Example

<CodeExample path={frontMatter.examples + '/basic.py'} language="python" />

<Image src={frontMatter.example_images + '/basic.png'} alt="basic" width="50%" caption="After clicking Submit" />

### Handling events

<CodeExample path={frontMatter.examples + '/handling_events.py'} language="python" />

<Image src={frontMatter.example_images + '/handling_events.png'} alt="handling-events" width="50%" caption="After three clicks" />

### Styled checkboxes

<CodeExample path={frontMatter.examples + '/styled.py'} language="python" />

<Image src={frontMatter.example_images + '/styled_checkboxes.png'} alt="Styled checkboxes" width="50%" />

<ClassMembers name={frontMatter.class_name} />

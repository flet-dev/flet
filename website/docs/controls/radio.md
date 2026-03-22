---
class_name: "flet.Radio"
examples: "../../examples/controls/radio"
example_images: "../test-images/examples/material/golden/macos/radio"
title: "Radio"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Simple radio buttons" />

## Examples

[Live example](https://flet-controls-gallery.fly.dev/input/radio)

### Basic Example

<CodeExample path={frontMatter.examples + '/basic.py'} />

<Image src={frontMatter.example_images + '/basic.png'} alt="basic" width="80%" />

### Handling selection changes

<CodeExample path={frontMatter.examples + '/handling_selection_changes.py'} />

<Image src={frontMatter.example_images + '/handling_selection_changes.png'} alt="handling-selection-changes" width="80%" />

### Styled radio buttons

<CodeExample path={frontMatter.examples + '/styled.py'} />

<ClassMembers name={frontMatter.class_name} />

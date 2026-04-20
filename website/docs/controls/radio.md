---
class_name: "flet.Radio"
examples: "controls/material/radio"
example_images: "test-images/examples/controls/material/golden/macos/radio"
title: "Radio"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Simple radio buttons" imageWidth="80%"/>

## Examples

[Live example](https://flet-controls-gallery.fly.dev/input/radio)

### Basic Example

<CodeExample path={frontMatter.examples + '/basic/main.py'} language="python" />

<Image src={frontMatter.example_images + '/basic.gif'} alt="basic" width="40%" />

### Handling selection changes

<CodeExample path={frontMatter.examples + '/handling_selection_changes/main.py'} language="python" />

<Image src={frontMatter.example_images + '/handling_selection_changes.gif'} alt="handling-selection-changes" width="40%" />

### Styled radio buttons

<CodeExample path={frontMatter.examples + '/styled/main.py'} language="python" />

<ClassMembers name={frontMatter.class_name} />

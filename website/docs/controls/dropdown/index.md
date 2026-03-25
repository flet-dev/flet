---
class_name: "flet.Dropdown"
examples: "controls/dropdown"
example_images: "../../test-images/examples/material/golden/macos/dropdown"
example_media: "../../examples/controls/dropdown/media"
title: "Dropdown"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

# Dropdown

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Basic Dropdown" />

## Examples

[Live example](https://flet-controls-gallery.fly.dev/input/dropdown)

### Color selection with filtering

<CodeExample path={frontMatter.examples + '/color_selection_with_filtering.py'} language="python" />

<Image src={frontMatter.example_media + '/color_selection_with_filtering.gif'} alt="color-selection-with-filtering" width="55%" />

### Icon selection

<CodeExample path={frontMatter.examples + '/icon_selection.py'} language="python" />

<Image src={frontMatter.example_media + '/icon_selection.png'} alt="icon-selection" width="55%" />

### Styled dropdowns

<CodeExample path={frontMatter.examples + '/styled.py'} language="python" />

<ClassMembers name={frontMatter.class_name} />

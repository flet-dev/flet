---
class_name: "flet.Dropdown"
examples: "controls/material/dropdown"
example_images: "test-images/examples/controls/material/golden/macos/dropdown"
title: "Dropdown"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

# Dropdown

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Basic Dropdown" imageWidth="25%"/>

## Examples

[Live example](https://flet-controls-gallery.fly.dev/input/dropdown)

### Color selection with filtering

<CodeExample path={frontMatter.examples + '/color_selection_with_filtering/main.py'} language="python" />

<Image src={frontMatter.example_images + '/color_selection_with_filtering_flow.gif'} alt="color-selection-with-filtering" width="35%" />

### Icon selection

<CodeExample path={frontMatter.examples + '/icon_selection/main.py'} language="python" />

<Image src={frontMatter.example_images + '/icon_selection_flow.gif'} alt="icon-selection" width="35%" />

### Declarative dropdown

<CodeExample path={frontMatter.examples + '/declarative/main.py'} language="python" />

<Image src={frontMatter.example_images + '/declarative_flow.gif'} alt="declarative-dropdown" width="35%" />

### Select and change events

<CodeExample path={frontMatter.examples + '/select_and_change_events/main.py'} language="python" />

<Image src={frontMatter.example_images + '/select_and_change_events_flow.gif'} alt="select-and-change-events" width="35%" />

### Styled dropdowns

<CodeExample path={frontMatter.examples + '/styled/main.py'} language="python" />

<Image src={frontMatter.example_images + '/styled_flow.gif'} alt="styled-dropdowns" width="35%" />

<ClassMembers name={frontMatter.class_name} />

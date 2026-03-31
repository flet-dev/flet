---
class_name: "flet.Tabs"
examples: "controls/tabs"
example_images: "examples/controls/tabs/media"
title: "Tabs"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

# Tabs

<ClassSummary name={frontMatter.class_name} />

## Examples

[Live example](https://flet-controls-gallery.fly.dev/layout/tabs)

### Basic Example

<CodeExample path={frontMatter.examples + '/basic.py'} language="python" />

<Image src={frontMatter.example_images + '/basic.gif'} width="55%" />

### Nesting tabs

<CodeExample path={frontMatter.examples + '/nested.py'} language="python" />

### Dynamic tab addition

<CodeExample path={frontMatter.examples + '/dynamic_tab_addition.py'} language="python" />

### Custom indicator

<CodeExample path={frontMatter.examples + '/custom_indicator.py'} language="python" />

### Programmatical Tab switch

<CodeExample path={frontMatter.examples + '/move_to.py'} language="python" />

<ClassMembers name={frontMatter.class_name} />

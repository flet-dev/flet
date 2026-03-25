---
class_name: "flet.Row"
examples: "controls/row"
example_images: "test-images/examples/core/golden/macos/row"
title: "Row"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Basic row of controls" />

## Examples

[Live example](https://flet-controls-gallery.fly.dev/layout/row)

### Spacing children

<CodeExample path={frontMatter.examples + '/spacing.py'} language="python" />

<Image src={frontMatter.example_images + '/row_spacing_adjustment.gif'} alt="spacing" width="55%" />

### Wrapping children

<CodeExample path={frontMatter.examples + '/wrap.py'} language="python" />

<Image src={frontMatter.example_images + '/wrap_adjustment.gif'} alt="wrap" width="55%" />

### Setting horizontal alignment

<CodeExample path={frontMatter.examples + '/alignment.py'} language="python" />

<Image src={frontMatter.example_images + '/alignment.png'} alt="alignment" width="40%" />

### Setting vertical alignment

<CodeExample path={frontMatter.examples + '/vertical_alignment.py'} language="python" />

<Image src={frontMatter.example_images + '/vertical_alignment.png'} alt="vertical-alignment" width="40%" />

<ClassMembers name={frontMatter.class_name} />

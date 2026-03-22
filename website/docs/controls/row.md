---
class_name: "flet.Row"
examples: "../../examples/controls/row"
example_images: "../test-images/examples/core/golden/macos/row"
title: "Row"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Basic row of controls" />

## Examples

[Live example](https://flet-controls-gallery.fly.dev/layout/row)

### Spacing children

<CodeExample path={frontMatter.examples + '/spacing.py'} />

<Image src={frontMatter.example_images + '/row_spacing_adjustment.gif'} alt="spacing" width="80%" />

### Wrapping children

<CodeExample path={frontMatter.examples + '/wrap.py'} />

<Image src={frontMatter.example_images + '/wrap_adjustment.gif'} alt="wrap" width="80%" />

### Setting horizontal alignment

<CodeExample path={frontMatter.examples + '/alignment.py'} />

<Image src={frontMatter.example_images + '/alignment.png'} alt="alignment" width="60%" />

### Setting vertical alignment

<CodeExample path={frontMatter.examples + '/vertical_alignment.py'} />

<Image src={frontMatter.example_images + '/vertical_alignment.png'} alt="vertical-alignment" width="60%" />

<ClassMembers name={frontMatter.class_name} />

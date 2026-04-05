---
class_name: "flet.Row"
examples: "controls/row"
example_images: "test-images/examples/core/golden/macos/row"
title: "Row"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Basic row of controls" imageWidth="60%"/>

## Examples

[Live example](https://flet-controls-gallery.fly.dev/layout/row)

### Spacing children

<CodeExample path={frontMatter.examples + '/spacing/main.py'} language="python" />

<Image src={frontMatter.example_images + '/row_spacing_adjustment.gif'} alt="spacing" width="70%" />

### Wrapping children

<CodeExample path={frontMatter.examples + '/wrap/main.py'} language="python" />

<Image src={frontMatter.example_images + '/wrap_adjustment.gif'} alt="wrap" width="70%" />

### Setting horizontal alignment

<CodeExample path={frontMatter.examples + '/alignment/main.py'} language="python" />

<Image src={frontMatter.example_images + '/alignment.png'} alt="alignment" width="28%" />

### Setting vertical alignment

<CodeExample path={frontMatter.examples + '/vertical_alignment/main.py'} language="python" />

<Image src={frontMatter.example_images + '/vertical_alignment.png'} alt="vertical-alignment" width="23%" />

<ClassMembers name={frontMatter.class_name} />

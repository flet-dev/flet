---
class_name: "flet.DatePicker"
examples: "controls/material/date_picker"
example_images: "test-images/examples/controls/material/golden/macos/date_picker"
title: "DatePicker"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Date picker" imageWidth="45%"/>

## Examples

[Live example](https://flet-controls-gallery.fly.dev/dialogs/datepicker)

### Basic Example

<CodeExample path={frontMatter.examples + '/basic/main.py'} language="python" />

<Image src={frontMatter.example_images + '/basic.png'} alt="basic" width="45%" />

### Custom locale

<CodeExample path={frontMatter.examples + '/custom_locale/main.py'} language="python" />

<Image src={frontMatter.example_images + '/custom_locale.png'} alt="custom-locale" width="45%" />

<ClassMembers name={frontMatter.class_name} />

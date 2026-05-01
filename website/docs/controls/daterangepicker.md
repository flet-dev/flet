---
class_name: "flet.DateRangePicker"
examples: "controls/material/date_range_picker"
example_images: "test-images/examples/controls/material/golden/macos/date_range_picker"
title: "DateRangePicker"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Date range picker" imageWidth="55%"/>

## Examples

[Live example](https://flet-controls-gallery.fly.dev/dialogs/daterangepicker)

### Basic Example

<CodeExample path={frontMatter.examples + '/basic/main.py'} language="python" />

<Image src={frontMatter.example_images + '/basic.png'} alt="basic" width="55%" />

### Custom locale

<CodeExample path={frontMatter.examples + '/custom_locale/main.py'} language="python" />

<Image src={frontMatter.example_images + '/custom_locale.png'} alt="custom-locale" width="55%" />

<ClassMembers name={frontMatter.class_name} />

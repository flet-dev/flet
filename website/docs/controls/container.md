---
class_name: "flet.Container"
examples: "controls/core/container"
example_media: "examples/controls/core/container/media"
example_images: "test-images/examples/controls/core/golden/macos/container"
title: "Container"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_media + '/overview_padding_margin_border.png'} imageCaption="Container explained" />

## Examples

<CodeExample path={frontMatter.examples + '/clickable/main.py'} language="python" />

<Image src={frontMatter.example_media + '/clickable.gif'} width="65%" />

<CodeExample path={frontMatter.examples + '/handling_clicks/main.py'} language="python" />

<Image src={frontMatter.example_media + '/handling_clicks.gif'} width="40%" />

<CodeExample path={frontMatter.examples + '/handling_hovers/main.py'} language="python" />

<Image src={frontMatter.example_media + '/handling_hovers.gif'} width="15%" />

<CodeExample path={frontMatter.examples + '/animate_size_and_color/main.py'} language="python" />

<Image src={frontMatter.example_media + '/animate_1.gif'} width="25%" />

<CodeExample path={frontMatter.examples + '/animate_gradient_and_shape/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/animated_slide_in_menu/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/inherited_and_overridden_theme/main.py'} language="python" />

<Image src={frontMatter.example_images + '/nested_themes_1.png'} width="40%" />

<CodeExample path={frontMatter.examples + '/page_dark_and_light_themes/main.py'} language="python" />

<Image src={frontMatter.example_images + '/nested_themes_2.png'} width="60%" />

<CodeExample path={frontMatter.examples + '/theme_mode_toggle/main.py'} language="python" />

<Image src={frontMatter.example_media + '/nested_themes_3.gif'} width="40%" />

<CodeExample path={frontMatter.examples + '/size_aware/main.py'} language="python" />

<Image src={frontMatter.example_images + '/size_aware.png'} width="40%" />

<ClassMembers name={frontMatter.class_name} />

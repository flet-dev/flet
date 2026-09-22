---
class_name: "flet.Icon"
examples: "controls/core/icon"
example_images: "test-images/examples/controls/core/golden/macos/icon"
example_media: "examples/controls/core/icon/media"
title: "Icon"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Icon" imageWidth="5%"/>

## Examples

To browse and visualize every available icon, see [Icons](../types/icons.md) and
[CupertinoIcons](../types/cupertinoicons.md) - or run the
[icons browser](https://studio.flet.dev/gallery/run/apps/icons_browser/) as a live Flet app.

<CodeExample path={frontMatter.examples + '/icon/main.py'} language="python" />

<Image src={frontMatter.example_media + '/basic.png'} alt="basic" width="25%" />

<ClassMembers name={frontMatter.class_name} />

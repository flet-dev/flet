---
class_name: "flet.Column"
examples: "controls/core/column"
example_images: "test-images/examples/controls/core/golden/macos/column"
example_media: "examples/controls/core/column/media"
title: "Column"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Basic Column with Text controls" imageWidth="25%"/>

## Examples

[Live example](https://flet-controls-gallery.fly.dev/layout/column)

### Column `spacing`

<CodeExample path={frontMatter.examples + '/spacing/main.py'} language="python" />

<Image src={frontMatter.example_media + '/spacing.gif'} alt="spacing" width="55%" />

### Column wrapping

<CodeExample path={frontMatter.examples + '/wrap/main.py'} language="python" />

<Image src={frontMatter.example_media + '/wrap.gif'} alt="wrap" width="55%" />

### Column vertical alignments

<CodeExample path={frontMatter.examples + '/alignment/main.py'} language="python" />

<Image src={frontMatter.example_media + '/alignment.png'} alt="alignment" width="55%" />

### Column horizontal alignments

<CodeExample path={frontMatter.examples + '/horizontal_alignment/main.py'} language="python" />

<Image src={frontMatter.example_media + '/horizontal_alignment.png'} alt="horizontal-alignment" width="40%" />

### Infinite scrolling

This example demonstrates adding of list items on-the-fly, as user scroll to the bottom,
creating the illusion of infinite list:

<CodeExample path={frontMatter.examples + '/infinite_scrolling/main.py'} language="python" />

### Scrolling programmatically

This example shows how to use [`scroll_to()`](column.md) to programmatically scroll a column:

<CodeExample path={frontMatter.examples + '/programmatic_scroll/main.py'} language="python" />

<Image src={frontMatter.example_media + '/programmatic_scroll.png'} alt="programmatic-scroll" width="55%" />

[//]: # (### Custom scrollbar)

<ClassMembers name={frontMatter.class_name} />

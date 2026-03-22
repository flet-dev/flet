---
class_name: "flet.Column"
examples: "../../examples/controls/column"
example_images: "../test-images/examples/core/golden/macos/column"
example_media: "../examples/controls/column/media"
title: "Column"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Basic Column with Text controls" />

## Examples

[Live example](https://flet-controls-gallery.fly.dev/layout/column)

### Column `spacing`

<CodeExample path={frontMatter.examples + '/spacing.py'} />

<Image src={frontMatter.example_media + '/spacing.gif'} alt="spacing" width="80%" />

### Column wrapping

<CodeExample path={frontMatter.examples + '/wrap.py'} />

<Image src={frontMatter.example_media + '/wrap.gif'} alt="wrap" width="80%" />

### Column vertical alignments

<CodeExample path={frontMatter.examples + '/alignment.py'} />

<Image src={frontMatter.example_media + '/alignment.png'} alt="alignment" width="80%" />

### Column horizontal alignments

<CodeExample path={frontMatter.examples + '/horizontal_alignment.py'} />

<Image src={frontMatter.example_media + '/horizontal_alignment.png'} alt="horizontal-alignment" width="80%" />

### Infinite scrolling

This example demonstrates adding of list items on-the-fly, as user scroll to the bottom,
creating the illusion of infinite list:

<CodeExample path={frontMatter.examples + '/infinite_scrolling.py'} />

### Scrolling programmatically

This example shows how to use [`scroll_to()`][flet.Column.scroll_to] to programmatically scroll a column:

<CodeExample path={frontMatter.examples + '/programmatic_scroll.py'} />

<Image src={frontMatter.example_media + '/programmatic_scroll.png'} alt="programmatic-scroll" width="80%" />

[//]: # (### Custom scrollbar)

<ClassMembers name={frontMatter.class_name} />

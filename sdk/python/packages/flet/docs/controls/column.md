---
class_name: flet.Column
examples: ../../examples/controls/column
example_images: ../test-images/examples/core/golden/macos/column
---

{{ class_summary(class_name, example_images + "/image_for_docs.png", image_caption="Basic Column with Text controls") }}

## Examples

### Column `spacing`

{{ code_and_demo(examples + "/spacing.py", demo_height="420", demo_width="80%") }}

### Column wrapping

{{ code_and_demo(examples + "/wrap.py", demo_height="420", demo_width="80%") }}

### Column vertical alignments

{{ code_and_demo(examples + "/alignment.py", demo_height="420", demo_width="80%") }}

### Column horizontal alignments

{{ code_and_demo(examples + "/horizontal_alignment.py", demo_height="420", demo_width="80%") }}

### Infinite scrolling

This example demonstrates adding of list items on-the-fly, as user scroll to the bottom,
creating the illusion of infinite list:

{{ code_and_demo(examples + "/infinite_scrolling.py", demo_height="420", demo_width="80%") }}

### Scrolling programmatically

This example shows how to use [`scroll_to()`][flet.Column.scroll_to] to programmatically scroll a column:

{{ code_and_demo(examples + "/programmatic_scroll.py", demo_height="420", demo_width="80%") }}


[//]: # (### Custom scrollbar)

{{ class_members(class_name) }}

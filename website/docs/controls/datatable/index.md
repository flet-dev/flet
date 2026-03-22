---
class_name: "flet.DataTable"
examples: "../../examples/controls/data_table"
example_images: "../../test-images/examples/material/golden/macos/datatable"
title: "DataTable"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

# DataTable

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Basic DataTable" />

## Examples

[Live example](https://flet-controls-gallery.fly.dev/layout/datatable)

### Basic Example

<CodeExample path={frontMatter.examples + '/basic.py'} />

<Image src={frontMatter.example_images + '/basic.png'} width="80%" />

### Horizontal margin and column spacing

Use [`horizontal_margin`][flet.DataTable.horizontal_margin] to control the left and right
edge spacing of the first and last columns.
Use [`column_spacing`][flet.DataTable.column_spacing] to control spacing between columns.

<CodeExample path={frontMatter.examples + '/spacing.py'} />

### Adaptive row heights

Setting [`data_row_max_height`][flet.DataTable.data_row_max_height] to `float('inf')`
(infinity) will cause the `DataTable` to let each individual row adapt its height to its
respective content, instead of all rows having the same height.

<CodeExample path={frontMatter.examples + '/adaptive_row_heights.py'} />

### Sortable columns and selectable rows

This example demonstrates row selection (including select-all),
sortable string and numeric columns, and stable selection across sorts and refreshes.

<CodeExample path={frontMatter.examples + '/sortable_and_selectable.py'} />

<Image src={frontMatter.example_images + '/sortable_and_selectable.png'} width="80%" />

### Handling events

<CodeExample path={frontMatter.examples + '/handling_events.py'} />

<ClassMembers name={frontMatter.class_name} />

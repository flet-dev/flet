---
examples: "controls/datatable2"
example_media: "examples/controls/datatable2/media"
title: "Overview"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';
import {ClassAll, CodeExample, Image} from '@site/src/components/crocodocs';

# DataTable2

Enhanced data table for [Flet](https://flet.dev) that adds sticky headers, fixed rows/columns, and other UX improvements via the `flet-datatable2` extension.

It wraps the Flutter [`data_table_2`](https://pub.dev/packages/data_table_2) package.

## Platform Support

| Platform  | Windows | macOS | Linux | iOS | Android | Web |
|-----------|---------|-------|-------|-----|---------|-----|
| Supported | ✅       | ✅     | ✅     | ✅   | ✅       | ✅   |

## Usage

Add `flet-datatable2` to your project dependencies:

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```bash
uv add flet-datatable2
```

</TabItem>
<TabItem value="pip" label="pip">
```bash
pip install flet-datatable2  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
</TabItem>
</Tabs>
## Examples

### Example 1

<CodeExample path={frontMatter.examples + '/example_1/main.py'} language="python" />

### Example 2

<CodeExample path={frontMatter.examples + '/example_2/main.py'} language="python" />

<Image src={frontMatter.example_media + '/example_2.gif'} width="55%" />

## Description

<ClassAll name="flet_datatable2.DataTable2" />

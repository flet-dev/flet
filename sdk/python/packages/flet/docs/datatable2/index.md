---
examples: ../../examples/controls/datatable2
---

# DataTable2

Enhanced data table for [Flet](https://flet.dev) that adds sticky headers, fixed rows/columns, and other UX improvements via the `flet-datatable2` extension.

It wraps the Flutter [`data_table_2`](https://pub.dev/packages/data_table_2) package.

## Platform Support

| Platform  | Windows | macOS | Linux | iOS | Android | Web |
|-----------|---------|-------|-------|-----|---------|-----|
| Supported | ✅       | ✅     | ✅     | ✅   | ✅       | ✅   |

## Usage

Add `flet-datatable2` to your project dependencies:

/// tab | uv
```bash
uv add flet-datatable2
```

///
/// tab | pip
```bash
pip install flet-datatable2  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
///

## Examples

### Example 1

{{ code_and_demo(examples + "/example_1.py", demo_height="420", demo_width="80%") }}

### Example 2

{{ code_and_demo(examples + "/example_2.py", demo_height="420", demo_width="80%") }}

## Description

{{ class_all_options("flet_datatable2.DataTable2") }}

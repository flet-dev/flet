---
examples: ../../examples/controls/datatable2
---

# DataTable2

Enhanced data table for [Flet](https://flet.dev) that adds sticky headers, fixed rows/columns, and other UX improvements via the `flet-datatable2` extension.

It wraps the Flutter [`data_table_2`](https://pub.dev/packages/data_table_2) package.

## Platform Support

| Platform | Windows | macOS | Linux | iOS | Android | Web |
|----------|---------|-------|-------|-----|---------|-----|
| Supported|    ✅    |   ✅   |   ✅   |  ✅  |    ✅    |  ✅  |

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

## Example

```python
--8<-- "{{ examples }}/example_1.py"
```

```python
--8<-- "{{ examples }}/example_2.py"
```

![DataTable2 example]({{ examples }}/media/example_2.gif)

## Description

{{ class_all_options("flet_datatable2.DataTable2") }}

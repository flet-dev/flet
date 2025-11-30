---
class_name: flet_lottie.Lottie
examples: ../../examples/controls/lottie
---

# Lottie

Render rich [Lottie](https://airbnb.design/lottie/) animations inside your [Flet](https://flet.dev) apps with a simple control.

It is backed by the [lottie](https://pub.dev/packages/lottie) Flutter package.

## Platform Support

| Platform  | Windows | macOS | Linux | iOS | Android | Web |
|-----------|---------|-------|-------|-----|---------|-----|
| Supported | ✅       | ✅     | ✅     | ✅   | ✅       | ✅   |

## Usage

Add the `flet-lottie` package to your project dependencies:

/// tab | uv
```bash
uv add flet-lottie
```

///
/// tab | pip
```bash
pip install flet-lottie  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
///

## Example

{{ code_and_demo(examples + "/basic.py", demo_height="420", demo_width="100%") }}

## Description

{{ class_all_options(class_name) }}

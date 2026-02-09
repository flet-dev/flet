---
examples: ../../examples/controls/map
---

# Map

Display interactive maps in your [Flet](https://flet.dev) apps with markers, overlays, and rich attributions provided by the `flet-map` extension. The control is built on top of [`flutter_map`](https://pub.dev/packages/flutter_map) and supports multiple tile providers and layers.

## Platform Support

| Platform | Windows | macOS | Linux | iOS | Android | Web |
|----------|---------|-------|-------|-----|---------|-----|
| Supported|    ✅    |   ✅   |   ✅   |  ✅  |    ✅    |  ✅  |

## Usage

Add the `flet-map` package to your project dependencies:

/// tab | uv
```bash
uv add flet-map
```

///
/// tab | pip
```bash
pip install flet-map  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
///

> Different tile providers have their own usage policies. Make sure you comply with their attribution and rate limits.

## Example

```python
--8<-- "{{ examples }}/example_1.py"
```

## Reference

- [`Map`](map.md)
- Layers: [`TileLayer`](tilelayer.md), [`MarkerLayer`](markerlayer.md), [`CircleLayer`](circlelayer.md), [`PolygonLayer`](polygonlayer.md), [`PolylineLayer`](polylinelayer.md)
- Markers and overlays: [`Marker`](marker.md), [`CircleMarker`](circlemarker.md), [`PolygonMarker`](polygonmarker.md), [`PolylineMarker`](polylinemarker.md)
- Attributions: [`SimpleAttribution`](simpleattribution.md), [`RichAttribution`](richattribution.md), [`SourceAttribution`](sourceattribution.md)

See the [types](types/attributionalignment.md) section for additional configuration helpers.

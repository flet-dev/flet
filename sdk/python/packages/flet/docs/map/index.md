---
examples: ../../examples/controls/map
---

# Map

Display interactive maps in your [Flet](https://flet.dev) apps with markers, overlays, and rich attributions provided by the `flet-map` extension. The control is built on top of [`flutter_map`](https://pub.dev/packages/flutter_map) and supports multiple tile providers and layers.

## Platform Support

| Platform  | Windows | macOS | Linux | iOS | Android | Web |
|-----------|---------|-------|-------|-----|---------|-----|
| Supported | ✅       | ✅     | ✅     | ✅   | ✅       | ✅   |

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

{{ code_and_demo(examples + "/example_1.py", demo_height="420", demo_width="100%") }}

## Reference

- [`Map`](map.md)
- Layers: [`TileLayer`](tile_layer.md), [`MarkerLayer`](marker_layer.md), [`CircleLayer`](circle_layer.md), [`PolygonLayer`](polygon_layer.md), [`PolylineLayer`](polyline_layer.md)
- Markers and overlays: [`Marker`](marker.md), [`CircleMarker`](circle_marker.md), [`PolygonMarker`](polygon_marker.md), [`PolylineMarker`](polyline_marker.md)
- Attributions: [`SimpleAttribution`](simple_attribution.md), [`RichAttribution`](rich_attribution.md), [`SourceAttribution`](source_attribution.md)

See the [types](types/attribution_alignment.md) section for additional configuration helpers.

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

/// admonition | Important
    type: danger
Different tile providers have their own usage policies.
Make sure you fully comply with their requirements (ex: attribution, rate limits)
when using them in your app, to avoid being blocked or facing legal issues.
More details [here](tilelayer.md).
///

## Examples

### Basic

```python
--8<-- "{{ examples }}/basic.py"
```

### Camera Controls

```python
--8<-- "{{ examples }}/camera_controls.py"
```

### Idle Camera

```python
--8<-- "{{ examples }}/idle_camera.py"
```

### Interaction Flags

```python
--8<-- "{{ examples }}/interaction_flags.py"
```

### Multiple Layers

```python
--8<-- "{{ examples }}/multi_layers.py"
```

## Reference

- [`Map`](map.md)
- Layers: [`TileLayer`](tilelayer.md), [`MarkerLayer`](markerlayer.md), [`CircleLayer`](circlelayer.md), [`PolygonLayer`](polygonlayer.md), [`PolylineLayer`](polylinelayer.md)
- Markers and overlays: [`Marker`](marker.md), [`CircleMarker`](circlemarker.md), [`PolygonMarker`](polygonmarker.md), [`PolylineMarker`](polylinemarker.md)
- Attributions: [`SimpleAttribution`](simpleattribution.md), [`RichAttribution`](richattribution.md), [`SourceAttribution`](sourceattribution.md)

See the [types](types/attributionalignment.md) section for additional configuration helpers.

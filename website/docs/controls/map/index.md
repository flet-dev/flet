---
examples: "controls/core/map"
title: "Overview"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';
import {CodeExample} from '@site/src/components/crocodocs';

# Map

Display interactive maps in your [Flet](https://flet.dev) apps with markers, overlays, and rich attributions provided by the `flet-map` extension. The control is built on top of [`flutter_map`](https://pub.dev/packages/flutter_map) and supports multiple tile providers and layers.

## Platform Support

| Platform  | Windows | macOS | Linux | iOS | Android | Web |
|-----------|---------|-------|-------|-----|---------|-----|
| Supported | ✅       | ✅     | ✅     | ✅   | ✅       | ✅   |

## Usage

Add the `flet-map` package to your project dependencies:

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```bash
uv add flet-map
```

</TabItem>
<TabItem value="pip" label="pip">
```bash
pip install flet-map  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
</TabItem>
</Tabs>
:::danger[Important]
Different tile providers have their own usage policies.
Make sure you fully comply with their requirements (ex: attribution, rate limits)
when using them in your app, to avoid being blocked or facing legal issues.
More details [here](tilelayer.md).
:::

## Examples

### Basic

<CodeExample path={frontMatter.examples + '/basic/main.py'} language="python" />

### Camera Controls

<CodeExample path={frontMatter.examples + '/camera_controls/main.py'} language="python" />

### Idle Camera

<CodeExample path={frontMatter.examples + '/idle_camera/main.py'} language="python" />

### Interaction Flags

<CodeExample path={frontMatter.examples + '/interaction_flags/main.py'} language="python" />

### Multiple Layers

<CodeExample path={frontMatter.examples + '/multi_layers/main.py'} language="python" />

## Reference

- [`Map`](mapcontrol.md)
- Layers: [`TileLayer`](tilelayer.md), [`MarkerLayer`](markerlayer.md), [`CircleLayer`](circlelayer.md), [`PolygonLayer`](polygonlayer.md), [`PolylineLayer`](polylinelayer.md)
- Markers and overlays: [`Marker`](marker.md), [`CircleMarker`](circlemarker.md), [`PolygonMarker`](polygonmarker.md), [`PolylineMarker`](polylinemarker.md)
- Attributions: [`SimpleAttribution`](simpleattribution.md), [`RichAttribution`](richattribution.md), [`SourceAttribution`](sourceattribution.md)

See the [types](types/attributionalignment.md) section for additional configuration helpers.

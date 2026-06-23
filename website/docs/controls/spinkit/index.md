---
examples: "extensions/spinkit"
title: "SpinKit"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';
import {CodeExample} from '@site/src/components/crocodocs';

# SpinKit

30 animated loading spinner controls built on Flutter's
[`flutter_spinkit`](https://pub.dev/packages/flutter_spinkit) package.

## Usage

Add `flet-spinkit` to your project dependencies:

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```bash
uv add flet-spinkit
```

</TabItem>
<TabItem value="pip" label="pip">
```bash
pip install flet-spinkit  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
</TabItem>
</Tabs>

Then import the package in your Flet app:

```python
import flet_spinkit as spins
```

### Boot screen

`flet-spinkit` also provides a [boot screen](../../publish/index.md#boot-screen) named
`spinkit` — an animated loader shown while your packaged app is starting up. Once
`flet-spinkit` is a dependency, select it in `pyproject.toml`:

```toml
[tool.flet.boot_screen]
name = "spinkit"

[tool.flet.boot_screen.spinkit]
spinner = "WanderingCubes"          # any SpinKit animation (without the "SpinKit" prefix)
spinner_color_light = "#7c4dff"
spinner_color_dark = "#b388ff"
spinner_size = 60
bgcolor_light = "#ffffff"
bgcolor_dark = "#0d0d12"
prepare_message = "Preparing your app…"
startup_message = "Starting up…"
```

All options are optional:

| Option | Default | Description |
|--------|---------|-------------|
| `spinner` | `WanderingCubes` | Any SpinKit animation, named without the `SpinKit` prefix (e.g. `Wave`, `FadingCube`, `PouringHourGlass`). Case-insensitive. |
| `theme_mode` | `auto` | `auto` (follow device), `light`, or `dark`. |
| `bgcolor_light` / `bgcolor_dark` | Flet theme background | Background color. |
| `spinner_color_light` / `spinner_color_dark` | Flet theme primary | Spinner color. |
| `spinner_size` | `60` | Spinner size in logical pixels. |
| `text_color_light` / `text_color_dark` | Flet theme on-surface | Message text color. |
| `prepare_message` | none | Text shown while unpacking the app (Android only). |
| `startup_message` | none | Text shown while the Python runtime and app start. |
| `fade_out_duration` | `0` | Fade-out duration in milliseconds when the app becomes ready; `0` removes it instantly. |

:::tip
This boot screen is a complete, real-world example of the
[`createBootScreen`](../../extend/user-extensions.md#boot-screen) extension hook —
see its source under `flet-spinkit`'s `src/flutter/flet_spinkit/lib/src/boot_screen.dart`.
:::

## Examples

<CodeExample path={frontMatter.examples + '/spinkit_showcase/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/spinkit_props/main.py'} language="python" />

## Available controls

- [ChasingDots](chasingdots.md)
- [Circle](circle.md)
- [CubeGrid](cubegrid.md)
- [DancingSquare](dancingsquare.md)
- [DoubleBounce](doublebounce.md)
- [DualRing](dualring.md)
- [FadingCircle](fadingcircle.md)
- [FadingCube](fadingcube.md)
- [FadingFour](fadingfour.md)
- [FadingGrid](fadinggrid.md)
- [FoldingCube](foldingcube.md)
- [HourGlass](hourglass.md)
- [PianoWave](pianowave.md)
- [PouringHourGlass](pouringhourglass.md)
- [PouringHourGlassRefined](pouringhourglassrefined.md)
- [Pulse](pulse.md)
- [PulsingGrid](pulsinggrid.md)
- [PumpingHeart](pumpingheart.md)
- [Ring](ring.md)
- [Ripple](ripple.md)
- [RotatingCircle](rotatingcircle.md)
- [RotatingPlain](rotatingplain.md)
- [SpinningCircle](spinningcircle.md)
- [SpinningLines](spinninglines.md)
- [SquareCircle](squarecircle.md)
- [ThreeBounce](threebounce.md)
- [ThreeInOut](threeinout.md)
- [WanderingCubes](wanderingcubes.md)
- [Wave](wave.md)
- [WaveSpinner](wavespinner.md)

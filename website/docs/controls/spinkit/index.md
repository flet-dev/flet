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

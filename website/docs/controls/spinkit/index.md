---
examples: "extensions/spinkit"
title: "SpinKit"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';
import {ClassMembers, ClassSummary, CodeExample} from '@site/src/components/crocodocs';

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
import flet_spinkit as fsk
```

## Examples

<CodeExample path={frontMatter.examples + '/spinkit_showcase/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/spinkit_props/main.py'} language="python" />

## Controls

All spinkit controls share these common properties:

| Property | Type | Default | Description |
|---|---|---|---|
| `color` | `ColorValue` | theme primary | Spinner color. |
| `size` | `Number` | `50` | Width and height in pixels. |
| `duration` | `DurationValue` | control-specific | Duration of one animation cycle. |

Some controls have additional properties listed in their section below.

---

### ChasingDots

<ClassSummary name="flet_spinkit.ChasingDots" />

<ClassMembers name="flet_spinkit.ChasingDots" />

---

### Circle

<ClassSummary name="flet_spinkit.Circle" />

<ClassMembers name="flet_spinkit.Circle" />

---

### CubeGrid

<ClassSummary name="flet_spinkit.CubeGrid" />

<ClassMembers name="flet_spinkit.CubeGrid" />

---

### DancingSquare

<ClassSummary name="flet_spinkit.DancingSquare" />

<ClassMembers name="flet_spinkit.DancingSquare" />

---

### DoubleBounce

<ClassSummary name="flet_spinkit.DoubleBounce" />

<ClassMembers name="flet_spinkit.DoubleBounce" />

---

### DualRing

<ClassSummary name="flet_spinkit.DualRing" />

<ClassMembers name="flet_spinkit.DualRing" />

---

### FadingCircle

<ClassSummary name="flet_spinkit.FadingCircle" />

<ClassMembers name="flet_spinkit.FadingCircle" />

---

### FadingCube

<ClassSummary name="flet_spinkit.FadingCube" />

<ClassMembers name="flet_spinkit.FadingCube" />

---

### FadingFour

<ClassSummary name="flet_spinkit.FadingFour" />

<ClassMembers name="flet_spinkit.FadingFour" />

---

### FadingGrid

<ClassSummary name="flet_spinkit.FadingGrid" />

<ClassMembers name="flet_spinkit.FadingGrid" />

---

### FoldingCube

<ClassSummary name="flet_spinkit.FoldingCube" />

<ClassMembers name="flet_spinkit.FoldingCube" />

---

### HourGlass

<ClassSummary name="flet_spinkit.HourGlass" />

<ClassMembers name="flet_spinkit.HourGlass" />

---

### PianoWave

<ClassSummary name="flet_spinkit.PianoWave" />

<ClassMembers name="flet_spinkit.PianoWave" />

---

### PouringHourGlass

<ClassSummary name="flet_spinkit.PouringHourGlass" />

<ClassMembers name="flet_spinkit.PouringHourGlass" />

---

### PouringHourGlassRefined

<ClassSummary name="flet_spinkit.PouringHourGlassRefined" />

<ClassMembers name="flet_spinkit.PouringHourGlassRefined" />

---

### Pulse

<ClassSummary name="flet_spinkit.Pulse" />

<ClassMembers name="flet_spinkit.Pulse" />

---

### PulsingGrid

<ClassSummary name="flet_spinkit.PulsingGrid" />

<ClassMembers name="flet_spinkit.PulsingGrid" />

---

### PumpingHeart

<ClassSummary name="flet_spinkit.PumpingHeart" />

<ClassMembers name="flet_spinkit.PumpingHeart" />

---

### Ring

<ClassSummary name="flet_spinkit.Ring" />

<ClassMembers name="flet_spinkit.Ring" />

---

### Ripple

<ClassSummary name="flet_spinkit.Ripple" />

<ClassMembers name="flet_spinkit.Ripple" />

---

### RotatingCircle

<ClassSummary name="flet_spinkit.RotatingCircle" />

<ClassMembers name="flet_spinkit.RotatingCircle" />

---

### RotatingPlain

<ClassSummary name="flet_spinkit.RotatingPlain" />

<ClassMembers name="flet_spinkit.RotatingPlain" />

---

### SpinningCircle

<ClassSummary name="flet_spinkit.SpinningCircle" />

<ClassMembers name="flet_spinkit.SpinningCircle" />

---

### SpinningLines

<ClassSummary name="flet_spinkit.SpinningLines" />

<ClassMembers name="flet_spinkit.SpinningLines" />

---

### SquareCircle

<ClassSummary name="flet_spinkit.SquareCircle" />

<ClassMembers name="flet_spinkit.SquareCircle" />

---

### ThreeBounce

<ClassSummary name="flet_spinkit.ThreeBounce" />

<ClassMembers name="flet_spinkit.ThreeBounce" />

---

### ThreeInOut

<ClassSummary name="flet_spinkit.ThreeInOut" />

<ClassMembers name="flet_spinkit.ThreeInOut" />

---

### WanderingCubes

<ClassSummary name="flet_spinkit.WanderingCubes" />

<ClassMembers name="flet_spinkit.WanderingCubes" />

---

### Wave

<ClassSummary name="flet_spinkit.Wave" />

<ClassMembers name="flet_spinkit.Wave" />

---

### WaveSpinner

<ClassSummary name="flet_spinkit.WaveSpinner" />

<ClassMembers name="flet_spinkit.WaveSpinner" />

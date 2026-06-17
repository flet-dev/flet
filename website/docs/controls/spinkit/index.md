---
examples: "extensions/spinkit"
example_images: "test-images/examples/extensions/spinkit/golden/macos/spinkit_showcase"
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

<ClassSummary name="flet_spinkit.ChasingDots" image={frontMatter.example_images + '/chasing_dots.png'} imageCaption="ChasingDots" imageWidth="25%" />

<ClassMembers name="flet_spinkit.ChasingDots" />

---

### Circle

<ClassSummary name="flet_spinkit.Circle" image={frontMatter.example_images + '/circle.png'} imageCaption="Circle" imageWidth="25%" />

<ClassMembers name="flet_spinkit.Circle" />

---

### CubeGrid

<ClassSummary name="flet_spinkit.CubeGrid" image={frontMatter.example_images + '/cube_grid.png'} imageCaption="CubeGrid" imageWidth="25%" />

<ClassMembers name="flet_spinkit.CubeGrid" />

---

### DancingSquare

<ClassSummary name="flet_spinkit.DancingSquare" image={frontMatter.example_images + '/dancing_square.png'} imageCaption="DancingSquare" imageWidth="25%" />

<ClassMembers name="flet_spinkit.DancingSquare" />

---

### DoubleBounce

<ClassSummary name="flet_spinkit.DoubleBounce" image={frontMatter.example_images + '/double_bounce.png'} imageCaption="DoubleBounce" imageWidth="25%" />

<ClassMembers name="flet_spinkit.DoubleBounce" />

---

### DualRing

<ClassSummary name="flet_spinkit.DualRing" image={frontMatter.example_images + '/dual_ring.png'} imageCaption="DualRing" imageWidth="25%" />

<ClassMembers name="flet_spinkit.DualRing" />

---

### FadingCircle

<ClassSummary name="flet_spinkit.FadingCircle" image={frontMatter.example_images + '/fading_circle.png'} imageCaption="FadingCircle" imageWidth="25%" />

<ClassMembers name="flet_spinkit.FadingCircle" />

---

### FadingCube

<ClassSummary name="flet_spinkit.FadingCube" image={frontMatter.example_images + '/fading_cube.png'} imageCaption="FadingCube" imageWidth="25%" />

<ClassMembers name="flet_spinkit.FadingCube" />

---

### FadingFour

<ClassSummary name="flet_spinkit.FadingFour" image={frontMatter.example_images + '/fading_four.png'} imageCaption="FadingFour" imageWidth="25%" />

<ClassMembers name="flet_spinkit.FadingFour" />

---

### FadingGrid

<ClassSummary name="flet_spinkit.FadingGrid" image={frontMatter.example_images + '/fading_grid.png'} imageCaption="FadingGrid" imageWidth="25%" />

<ClassMembers name="flet_spinkit.FadingGrid" />

---

### FoldingCube

<ClassSummary name="flet_spinkit.FoldingCube" image={frontMatter.example_images + '/folding_cube.png'} imageCaption="FoldingCube" imageWidth="25%" />

<ClassMembers name="flet_spinkit.FoldingCube" />

---

### HourGlass

<ClassSummary name="flet_spinkit.HourGlass" image={frontMatter.example_images + '/hour_glass.png'} imageCaption="HourGlass" imageWidth="25%" />

<ClassMembers name="flet_spinkit.HourGlass" />

---

### PianoWave

<ClassSummary name="flet_spinkit.PianoWave" image={frontMatter.example_images + '/piano_wave.png'} imageCaption="PianoWave" imageWidth="25%" />

<ClassMembers name="flet_spinkit.PianoWave" />

---

### PouringHourGlass

<ClassSummary name="flet_spinkit.PouringHourGlass" image={frontMatter.example_images + '/pouring_hour_glass.png'} imageCaption="PouringHourGlass" imageWidth="25%" />

<ClassMembers name="flet_spinkit.PouringHourGlass" />

---

### PouringHourGlassRefined

<ClassSummary name="flet_spinkit.PouringHourGlassRefined" image={frontMatter.example_images + '/pouring_hour_glass_refined.png'} imageCaption="PouringHourGlassRefined" imageWidth="25%" />

<ClassMembers name="flet_spinkit.PouringHourGlassRefined" />

---

### Pulse

<ClassSummary name="flet_spinkit.Pulse" image={frontMatter.example_images + '/pulse.png'} imageCaption="Pulse" imageWidth="25%" />

<ClassMembers name="flet_spinkit.Pulse" />

---

### PulsingGrid

<ClassSummary name="flet_spinkit.PulsingGrid" image={frontMatter.example_images + '/pulsing_grid.png'} imageCaption="PulsingGrid" imageWidth="25%" />

<ClassMembers name="flet_spinkit.PulsingGrid" />

---

### PumpingHeart

<ClassSummary name="flet_spinkit.PumpingHeart" image={frontMatter.example_images + '/pumping_heart.png'} imageCaption="PumpingHeart" imageWidth="25%" />

<ClassMembers name="flet_spinkit.PumpingHeart" />

---

### Ring

<ClassSummary name="flet_spinkit.Ring" image={frontMatter.example_images + '/ring.png'} imageCaption="Ring" imageWidth="25%" />

<ClassMembers name="flet_spinkit.Ring" />

---

### Ripple

<ClassSummary name="flet_spinkit.Ripple" image={frontMatter.example_images + '/ripple.png'} imageCaption="Ripple" imageWidth="25%" />

<ClassMembers name="flet_spinkit.Ripple" />

---

### RotatingCircle

<ClassSummary name="flet_spinkit.RotatingCircle" image={frontMatter.example_images + '/rotating_circle.png'} imageCaption="RotatingCircle" imageWidth="25%" />

<ClassMembers name="flet_spinkit.RotatingCircle" />

---

### RotatingPlain

<ClassSummary name="flet_spinkit.RotatingPlain" image={frontMatter.example_images + '/rotating_plain.png'} imageCaption="RotatingPlain" imageWidth="25%" />

<ClassMembers name="flet_spinkit.RotatingPlain" />

---

### SpinningCircle

<ClassSummary name="flet_spinkit.SpinningCircle" image={frontMatter.example_images + '/spinning_circle.png'} imageCaption="SpinningCircle" imageWidth="25%" />

<ClassMembers name="flet_spinkit.SpinningCircle" />

---

### SpinningLines

<ClassSummary name="flet_spinkit.SpinningLines" image={frontMatter.example_images + '/spinning_lines.png'} imageCaption="SpinningLines" imageWidth="25%" />

<ClassMembers name="flet_spinkit.SpinningLines" />

---

### SquareCircle

<ClassSummary name="flet_spinkit.SquareCircle" image={frontMatter.example_images + '/square_circle.png'} imageCaption="SquareCircle" imageWidth="25%" />

<ClassMembers name="flet_spinkit.SquareCircle" />

---

### ThreeBounce

<ClassSummary name="flet_spinkit.ThreeBounce" image={frontMatter.example_images + '/three_bounce.png'} imageCaption="ThreeBounce" imageWidth="25%" />

<ClassMembers name="flet_spinkit.ThreeBounce" />

---

### ThreeInOut

<ClassSummary name="flet_spinkit.ThreeInOut" image={frontMatter.example_images + '/three_in_out.png'} imageCaption="ThreeInOut" imageWidth="25%" />

<ClassMembers name="flet_spinkit.ThreeInOut" />

---

### WanderingCubes

<ClassSummary name="flet_spinkit.WanderingCubes" image={frontMatter.example_images + '/wandering_cubes.png'} imageCaption="WanderingCubes" imageWidth="25%" />

<ClassMembers name="flet_spinkit.WanderingCubes" />

---

### Wave

<ClassSummary name="flet_spinkit.Wave" image={frontMatter.example_images + '/wave.png'} imageCaption="Wave" imageWidth="25%" />

<ClassMembers name="flet_spinkit.Wave" />

---

### WaveSpinner

<ClassSummary name="flet_spinkit.WaveSpinner" image={frontMatter.example_images + '/wave_spinner.png'} imageCaption="WaveSpinner" imageWidth="25%" />

<ClassMembers name="flet_spinkit.WaveSpinner" />

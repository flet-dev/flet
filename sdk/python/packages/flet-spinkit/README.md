# flet-spinkit

Loading spinner animation controls for [Flet](https://flet.dev) apps, powered by the [`flutter_spinkit`](https://pub.dev/packages/flutter_spinkit) Flutter package.

## Installation

```bash
pip install flet-spinkit
```

## Usage

```python
import flet as ft
import flet_spinkit as fsk

def main(page: ft.Page):
    page.add(
        fsk.SpinKitRotatingCircle(color=ft.Colors.BLUE, size=50),
        fsk.SpinKitWave(color=ft.Colors.RED, size=50, wave_type=fsk.SpinKitWaveType.CENTER),
        fsk.SpinKitDualRing(color=ft.Colors.GREEN, size=50, line_width=5),
        fsk.SpinKitRipple(color=ft.Colors.PURPLE, size=100, border_width=4),
    )

ft.app(main)
```

## Available Controls

| Control | Extra properties |
|---|---|
| `SpinKitRotatingPlain` | — |
| `SpinKitDoubleBounce` | — |
| `SpinKitWave` | `wave_type`, `item_count` |
| `SpinKitWanderingCubes` | — |
| `SpinKitFadingFour` | — |
| `SpinKitFadingCube` | — |
| `SpinKitPulse` | — |
| `SpinKitChasingDots` | — |
| `SpinKitThreeBounce` | — |
| `SpinKitCircle` | — |
| `SpinKitCubeGrid` | — |
| `SpinKitFadingCircle` | — |
| `SpinKitRotatingCircle` | — |
| `SpinKitFoldingCube` | — |
| `SpinKitPumpingHeart` | — |
| `SpinKitHourGlass` | — |
| `SpinKitPouringHourGlass` | — |
| `SpinKitPouringHourGlassRefined` | — |
| `SpinKitFadingGrid` | — |
| `SpinKitRing` | `line_width` |
| `SpinKitRipple` | `border_width` |
| `SpinKitDualRing` | `line_width` |
| `SpinKitSpinningCircle` | — |
| `SpinKitSpinningLines` | `line_width` |
| `SpinKitSquareCircle` | — |
| `SpinKitThreeInOut` | — |
| `SpinKitDancingSquare` | — |
| `SpinKitPianoWave` | `item_count` |
| `SpinKitPulsingGrid` | — |
| `SpinKitPumpCurve` | — |
| `SpinKitRingCurve` | `line_width` |

All controls share these common properties:

| Property | Type | Description |
|---|---|---|
| `color` | `ColorValue` | Spinner color |
| `size` | `Number` | Spinner size in pixels (default: 50) |
| `duration` | `DurationValue` | Animation cycle duration |

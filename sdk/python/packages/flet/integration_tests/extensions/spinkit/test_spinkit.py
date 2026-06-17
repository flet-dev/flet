import flet_spinkit as fsk

import flet as ft


def test_wave_type_values():
    assert fsk.WaveType.START.value == "start"
    assert fsk.WaveType.CENTER.value == "center"
    assert fsk.WaveType.END.value == "end"


def test_basic_properties():
    ctrl = fsk.RotatingCircle(color=ft.Colors.BLUE, size=60)
    assert ctrl.color == ft.Colors.BLUE
    assert ctrl.size == 60
    assert ctrl.duration is None


def test_duration():
    d = ft.Duration(milliseconds=800)
    ctrl = fsk.Pulse(color=ft.Colors.RED, size=40, duration=d)
    assert ctrl.duration == d


def test_wave_extra_props():
    ctrl = fsk.Wave(
        color=ft.Colors.GREEN,
        size=50,
        wave_type=fsk.WaveType.CENTER,
        item_count=7,
    )
    assert ctrl.wave_type == fsk.WaveType.CENTER
    assert ctrl.item_count == 7


def test_piano_wave_item_count():
    ctrl = fsk.PianoWave(color=ft.Colors.TEAL, size=50, item_count=8)
    assert ctrl.item_count == 8


def test_ring_line_width():
    ctrl = fsk.Ring(color=ft.Colors.BLUE, size=50, line_width=10)
    assert ctrl.line_width == 10


def test_dual_ring_line_width():
    ctrl = fsk.DualRing(color=ft.Colors.BLUE, size=50, line_width=4)
    assert ctrl.line_width == 4


def test_spinning_lines_line_width():
    ctrl = fsk.SpinningLines(color=ft.Colors.BLUE, size=50, line_width=3)
    assert ctrl.line_width == 3


def test_ripple_border_width():
    ctrl = fsk.Ripple(color=ft.Colors.BLUE, size=50, border_width=8)
    assert ctrl.border_width == 8


def test_all_controls_instantiate():
    color = ft.Colors.BLUE
    size = 50
    controls = [
        fsk.ChasingDots(color=color, size=size),
        fsk.Circle(color=color, size=size),
        fsk.CubeGrid(color=color, size=size),
        fsk.DancingSquare(color=color, size=size),
        fsk.DoubleBounce(color=color, size=size),
        fsk.DualRing(color=color, size=size),
        fsk.FadingCircle(color=color, size=size),
        fsk.FadingCube(color=color, size=size),
        fsk.FadingFour(color=color, size=size),
        fsk.FadingGrid(color=color, size=size),
        fsk.FoldingCube(color=color, size=size),
        fsk.HourGlass(color=color, size=size),
        fsk.PianoWave(color=color, size=size),
        fsk.PouringHourGlass(color=color, size=size),
        fsk.PouringHourGlassRefined(color=color, size=size),
        fsk.Pulse(color=color, size=size),
        fsk.PulsingGrid(color=color, size=size),
        fsk.PumpingHeart(color=color, size=size),
        fsk.Ring(color=color, size=size),
        fsk.Ripple(color=color, size=size),
        fsk.RotatingCircle(color=color, size=size),
        fsk.RotatingPlain(color=color, size=size),
        fsk.SpinningCircle(color=color, size=size),
        fsk.SpinningLines(color=color, size=size),
        fsk.SquareCircle(color=color, size=size),
        fsk.ThreeBounce(color=color, size=size),
        fsk.ThreeInOut(color=color, size=size),
        fsk.WanderingCubes(color=color, size=size),
        fsk.Wave(color=color, size=size),
        fsk.WaveSpinner(color=color, size=size),
    ]
    assert len(controls) == 30

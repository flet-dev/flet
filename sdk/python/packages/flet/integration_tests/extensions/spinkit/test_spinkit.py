import flet_spinkit as spins

import flet as ft


def test_wave_type_values():
    assert spins.WaveType.START.value == "start"
    assert spins.WaveType.CENTER.value == "center"
    assert spins.WaveType.END.value == "end"


def test_basic_properties():
    ctrl = spins.RotatingCircle(color=ft.Colors.BLUE, size=60)
    assert ctrl.color == ft.Colors.BLUE
    assert ctrl.size == 60
    assert ctrl.duration is None


def test_duration():
    d = ft.Duration(milliseconds=800)
    ctrl = spins.Pulse(color=ft.Colors.RED, size=40, duration=d)
    assert ctrl.duration == d


def test_wave_extra_props():
    ctrl = spins.Wave(
        color=ft.Colors.GREEN,
        size=50,
        wave_type=spins.WaveType.CENTER,
        item_count=7,
    )
    assert ctrl.wave_type == spins.WaveType.CENTER
    assert ctrl.item_count == 7


def test_piano_wave_item_count():
    ctrl = spins.PianoWave(color=ft.Colors.TEAL, size=50, item_count=8)
    assert ctrl.item_count == 8


def test_ring_line_width():
    ctrl = spins.Ring(color=ft.Colors.BLUE, size=50, line_width=10)
    assert ctrl.line_width == 10


def test_dual_ring_line_width():
    ctrl = spins.DualRing(color=ft.Colors.BLUE, size=50, line_width=4)
    assert ctrl.line_width == 4


def test_spinning_lines_line_width():
    ctrl = spins.SpinningLines(color=ft.Colors.BLUE, size=50, line_width=3)
    assert ctrl.line_width == 3


def test_ripple_border_width():
    ctrl = spins.Ripple(color=ft.Colors.BLUE, size=50, border_width=8)
    assert ctrl.border_width == 8


def test_all_controls_instantiate():
    color = ft.Colors.BLUE
    size = 50
    controls = [
        spins.ChasingDots(color=color, size=size),
        spins.Circle(color=color, size=size),
        spins.CubeGrid(color=color, size=size),
        spins.DancingSquare(color=color, size=size),
        spins.DoubleBounce(color=color, size=size),
        spins.DualRing(color=color, size=size),
        spins.FadingCircle(color=color, size=size),
        spins.FadingCube(color=color, size=size),
        spins.FadingFour(color=color, size=size),
        spins.FadingGrid(color=color, size=size),
        spins.FoldingCube(color=color, size=size),
        spins.HourGlass(color=color, size=size),
        spins.PianoWave(color=color, size=size),
        spins.PouringHourGlass(color=color, size=size),
        spins.PouringHourGlassRefined(color=color, size=size),
        spins.Pulse(color=color, size=size),
        spins.PulsingGrid(color=color, size=size),
        spins.PumpingHeart(color=color, size=size),
        spins.Ring(color=color, size=size),
        spins.Ripple(color=color, size=size),
        spins.RotatingCircle(color=color, size=size),
        spins.RotatingPlain(color=color, size=size),
        spins.SpinningCircle(color=color, size=size),
        spins.SpinningLines(color=color, size=size),
        spins.SquareCircle(color=color, size=size),
        spins.ThreeBounce(color=color, size=size),
        spins.ThreeInOut(color=color, size=size),
        spins.WanderingCubes(color=color, size=size),
        spins.Wave(color=color, size=size),
        spins.WaveSpinner(color=color, size=size),
    ]
    assert len(controls) == 30

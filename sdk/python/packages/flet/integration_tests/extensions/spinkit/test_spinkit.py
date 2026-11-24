import flet_spinkit as spins
import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_rotating_circle(flet_app: ftt.FletTestApp):
    flet_app.page.clean()
    flet_app.page.add(spins.RotatingCircle(color=ft.Colors.BLUE, size=50, key="ctrl"))
    await flet_app.tester.pump(duration=ft.Duration(milliseconds=500))
    assert (await flet_app.tester.find_by_key("ctrl")).count == 1


@pytest.mark.asyncio(loop_scope="module")
async def test_wave_default(flet_app: ftt.FletTestApp):
    flet_app.page.clean()
    flet_app.page.add(spins.Wave(color=ft.Colors.BLUE, size=50, key="ctrl"))
    await flet_app.tester.pump(duration=ft.Duration(milliseconds=500))
    assert (await flet_app.tester.find_by_key("ctrl")).count == 1


@pytest.mark.asyncio(loop_scope="module")
async def test_wave_type(flet_app: ftt.FletTestApp):
    flet_app.page.clean()
    flet_app.page.add(
        spins.Wave(
            color=ft.Colors.BLUE,
            size=50,
            wave_type=spins.WaveType.CENTER,
            item_count=7,
            key="ctrl",
        )
    )
    await flet_app.tester.pump(duration=ft.Duration(milliseconds=500))
    assert (await flet_app.tester.find_by_key("ctrl")).count == 1


@pytest.mark.asyncio(loop_scope="module")
async def test_ring_line_width(flet_app: ftt.FletTestApp):
    flet_app.page.clean()
    flet_app.page.add(
        spins.Ring(color=ft.Colors.BLUE, size=50, line_width=10, key="ctrl")
    )
    await flet_app.tester.pump(duration=ft.Duration(milliseconds=500))
    assert (await flet_app.tester.find_by_key("ctrl")).count == 1


@pytest.mark.asyncio(loop_scope="module")
async def test_dual_ring_line_width(flet_app: ftt.FletTestApp):
    flet_app.page.clean()
    flet_app.page.add(
        spins.DualRing(color=ft.Colors.BLUE, size=50, line_width=4, key="ctrl")
    )
    await flet_app.tester.pump(duration=ft.Duration(milliseconds=500))
    assert (await flet_app.tester.find_by_key("ctrl")).count == 1


@pytest.mark.asyncio(loop_scope="module")
async def test_ripple_border_width(flet_app: ftt.FletTestApp):
    flet_app.page.clean()
    flet_app.page.add(
        spins.Ripple(color=ft.Colors.BLUE, size=50, border_width=8, key="ctrl")
    )
    await flet_app.tester.pump(duration=ft.Duration(milliseconds=500))
    assert (await flet_app.tester.find_by_key("ctrl")).count == 1


@pytest.mark.asyncio(loop_scope="module")
async def test_spinning_lines_line_width(flet_app: ftt.FletTestApp):
    flet_app.page.clean()
    flet_app.page.add(
        spins.SpinningLines(color=ft.Colors.BLUE, size=50, line_width=3, key="ctrl")
    )
    await flet_app.tester.pump(duration=ft.Duration(milliseconds=500))
    assert (await flet_app.tester.find_by_key("ctrl")).count == 1


@pytest.mark.asyncio(loop_scope="module")
async def test_piano_wave_item_count(flet_app: ftt.FletTestApp):
    flet_app.page.clean()
    flet_app.page.add(
        spins.PianoWave(color=ft.Colors.BLUE, size=50, item_count=8, key="ctrl")
    )
    await flet_app.tester.pump(duration=ft.Duration(milliseconds=500))
    assert (await flet_app.tester.find_by_key("ctrl")).count == 1


@pytest.mark.asyncio(loop_scope="module")
async def test_custom_duration(flet_app: ftt.FletTestApp):
    flet_app.page.clean()
    flet_app.page.add(
        spins.Pulse(
            color=ft.Colors.BLUE,
            size=50,
            duration=ft.Duration(milliseconds=400),
            key="ctrl",
        )
    )
    await flet_app.tester.pump(duration=ft.Duration(milliseconds=500))
    assert (await flet_app.tester.find_by_key("ctrl")).count == 1


@pytest.mark.asyncio(loop_scope="module")
async def test_all_controls_render(flet_app: ftt.FletTestApp):
    controls = [
        spins.ChasingDots,
        spins.Circle,
        spins.CubeGrid,
        spins.DancingSquare,
        spins.DoubleBounce,
        spins.DualRing,
        spins.FadingCircle,
        spins.FadingCube,
        spins.FadingFour,
        spins.FadingGrid,
        spins.FoldingCube,
        spins.HourGlass,
        spins.PianoWave,
        spins.PouringHourGlass,
        spins.PouringHourGlassRefined,
        spins.Pulse,
        spins.PulsingGrid,
        spins.PumpingHeart,
        spins.Ring,
        spins.Ripple,
        spins.RotatingCircle,
        spins.RotatingPlain,
        spins.SpinningCircle,
        spins.SpinningLines,
        spins.SquareCircle,
        spins.ThreeBounce,
        spins.ThreeInOut,
        spins.WanderingCubes,
        spins.Wave,
        spins.WaveSpinner,
    ]
    flet_app.page.clean()
    flet_app.page.add(
        # The wrapped row of all spinners is much taller than the test window;
        # host it in a scrollable column so the page doesn't overflow (an
        # overflow error fails the Flutter test process).
        ft.Column(
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            controls=[
                ft.Row(
                    wrap=True,
                    key="row",
                    controls=[cls(color=ft.Colors.BLUE, size=40) for cls in controls],
                )
            ],
        )
    )
    await flet_app.tester.pump(duration=ft.Duration(milliseconds=500))
    assert (await flet_app.tester.find_by_key("row")).count == 1

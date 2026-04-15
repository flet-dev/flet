import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.material.expansion_tile.basic import main as basic
from examples.controls.material.expansion_tile.borders import main as borders
from examples.controls.material.expansion_tile.custom_animations import (
    main as custom_animations,
)
from examples.controls.material.expansion_tile.programmatic_expansion import (
    main as programmatic_expansion,
)


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.ExpansionTile(
            width=400,
            title="Account",
            subtitle="Manage profile and security",
            expanded=True,
            controls=[
                ft.ListTile(title=ft.Text("Profile")),
                ft.ListTile(title=ft.Text("Security")),
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": basic.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app_function: ftt.FletTestApp):
    flet_app_function.assert_screenshot(
        test_basic.__name__,
        await flet_app_function.take_page_controls_screenshot(),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": borders.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_borders(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(460, 300)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "borders_closed",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    expand_icons = await flet_app_function.tester.find_by_icon(ft.Icons.EXPAND_MORE)
    assert expand_icons.count >= 1
    await flet_app_function.tester.tap(expand_icons.first)
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "borders_opened",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    flet_app_function.create_gif(
        ["borders_closed", "borders_opened"],
        "borders_flow",
        duration=1000,
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": custom_animations.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_custom_animations_default(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(460, 300)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    # Pre-tap frame — GIF will hold this for 2 s so the viewer sees the
    # expanded tile before the collapse starts.
    pre_tap_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio,
    )

    expand_icons = await flet_app_function.tester.find_by_icon(ft.Icons.EXPAND_MORE)
    assert expand_icons.count >= 1
    await flet_app_function.tester.tap(expand_icons.first)

    # ExpansionTile's default animation is 200 ms and renders at 60 Hz vsync,
    # so it produces ~12 distinct pixel-level states. Sample at ~vsync
    # spacing — no point oversampling, neighbors would be pixel-identical.
    frame_delays_ms = [0] + [17] * 13 + [50]
    animation_frames = await flet_app_function.page.take_animation(
        "default_animation",
        frame_delays_ms,
        pixel_ratio=flet_app_function.screenshots_pixel_ratio,
    )

    # Play back at 80 ms/frame, hold the first frame for 2 s and the final
    # settled frame for 3 s before the GIF loops.
    frames = [pre_tap_frame, *animation_frames]
    durations = [2000] + [80] * (len(animation_frames) - 1) + [3000]
    flet_app_function.create_gif(
        frames=frames,
        output_name="custom_animations_default",
        duration=durations,
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": programmatic_expansion.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_programmatic_expansion(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(520, 320)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    frame_delays_ms = [0] + [17] * 13 + [50]
    frames: list[bytes] = []
    durations: list[int] = []

    initial_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    flet_app_function.assert_screenshot(
        "programmatic_expansion_initial",
        initial_frame,
    )
    frames.append(initial_frame)
    durations.append(1200)

    collapse_button = await flet_app_function.tester.find_by_text("Collapse Tile")
    await flet_app_function.tester.mouse_hover(collapse_button)
    await flet_app_function.tester.pump_and_settle()
    hover_collapse_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    frames.append(hover_collapse_frame)
    durations.append(1000)

    await flet_app_function.tester.tap(collapse_button)
    collapse_animation_frames = await flet_app_function.page.take_animation(
        "programmatic_expansion_collapse",
        frame_delays_ms,
        pixel_ratio=flet_app_function.screenshots_pixel_ratio,
    )
    collapsed_frame = collapse_animation_frames[-1]
    flet_app_function.assert_screenshot(
        "programmatic_expansion_collapsed",
        collapsed_frame,
    )
    frames.extend(collapse_animation_frames)
    durations.extend([80] * (len(collapse_animation_frames) - 1) + [1000])

    expand_button = await flet_app_function.tester.find_by_text("Expand Tile")
    await flet_app_function.tester.mouse_hover(expand_button)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )
    durations.append(1000)

    await flet_app_function.tester.tap(expand_button)
    expand_animation_frames = await flet_app_function.page.take_animation(
        "programmatic_expansion_expand",
        frame_delays_ms,
        pixel_ratio=flet_app_function.screenshots_pixel_ratio,
    )
    frames.extend(expand_animation_frames)
    durations.extend([80] * (len(expand_animation_frames) - 1) + [1500])

    flet_app_function.create_gif(
        frames=frames,
        output_name="programmatic_expansion_flow",
        duration=durations,
    )

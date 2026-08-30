from pathlib import Path

import pytest

import examples.apps.todo.main as todo_basic
import flet as ft
import flet.testing as ftt


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": todo_basic.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_todo_basic(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(700, 700 * 0.625)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    assert (await flet_app_function.tester.find_by_text("Todos")).count == 1

    task_input = await flet_app_function.tester.find_by_key("new_task")
    assert task_input.count == 1

    add_button = await flet_app_function.tester.find_by_key("add_task")
    assert add_button.count == 1

    # TEMPORARY DIAGNOSTICS for the CI-only failure: reach into the live app
    # to observe Python-side state, and dump screenshots named *_actual.png so
    # the failure-artifact upload collects them.
    app = flet_app_function.page.controls[0].content  # SafeArea -> TodoApp
    diag_dir = Path(__file__).parent / "golden" / "macos" / "todo"
    diag_dir.mkdir(parents=True, exist_ok=True)

    async def diag(tag: str):
        counts = {}
        for n in ["Release new Flet", "Update docs", "Write a blog post"]:
            counts[n] = (await flet_app_function.tester.find_by_text(n)).count
        print(
            f"DIAG {tag}: value={app.new_task.value!r} "
            f"tasks={len(app.tasks.controls)} finds={counts}"
        )
        shot = await flet_app_function.page.take_screenshot(pixel_ratio=2.0)
        (diag_dir / f"todo_diag_{tag}_actual.png").write_bytes(shot)

    async def add_task(name: str):
        await flet_app_function.tester.enter_text(task_input, name)
        await flet_app_function.tester.pump_and_settle()
        await flet_app_function.tester.tap(add_button)
        await flet_app_function.tester.pump_and_settle()
        assert (await flet_app_function.tester.find_by_text(name)).count == 1

    await add_task("Release new Flet")
    await diag("add1")
    await add_task("Update docs")
    await add_task("Write a blog post")
    await diag("add3")

    # Second probe: by now any pending value sync has long arrived. If clicks
    # are delivered at all, this tap must create a task from the current
    # TextField text (whatever it is) or be a no-op on empty - either way the
    # task count printed next tells us whether "click" events work.
    await flet_app_function.tester.tap(add_button)
    await flet_app_function.tester.pump_and_settle()
    await diag("retap")

    for name in ["Release new Flet", "Update docs"]:
        task = await flet_app_function.tester.find_by_text(name)
        assert task.count == 1
        await flet_app_function.tester.tap(task)
        await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "todo_basic",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

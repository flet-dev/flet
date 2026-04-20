import asyncio

import pytest

import flet.testing as ftt
from examples.apps.declarative.use_dialog_basic import main as use_dialog_basic
from examples.apps.declarative.use_dialog_chained import main as use_dialog_chained
from examples.apps.declarative.use_dialog_multiple import main as use_dialog_multiple

# ``use_dialog_*`` examples don't define a ``main(page)`` with page.render; they
# export both ``App`` (component) and ``main`` (wrapper). We use the module's
# ``main`` directly.


# ---------------------------------------------------------------------------
# use_dialog_basic — single dialog, open/cancel/confirm
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": use_dialog_basic.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_use_dialog_basic(flet_app_function: ftt.FletTestApp):
    title = await flet_app_function.tester.find_by_text("Declarative Dialog Example")
    assert title.count == 1

    # Dialog not yet open
    dialog_title = await flet_app_function.tester.find_by_text("Delete report.pdf?")
    assert dialog_title.count == 0

    # Open dialog via "Delete File" button
    open_btn = await flet_app_function.tester.find_by_text("Delete File")
    assert open_btn.count == 1
    await flet_app_function.tester.tap(open_btn)
    await flet_app_function.tester.pump_and_settle()

    dialog_title = await flet_app_function.tester.find_by_text("Delete report.pdf?")
    assert dialog_title.count == 1
    cancel_btn = await flet_app_function.tester.find_by_text("Cancel")
    assert cancel_btn.count == 1

    # Dismiss via Cancel
    await flet_app_function.tester.tap(cancel_btn)
    await flet_app_function.tester.pump_and_settle()

    dialog_title = await flet_app_function.tester.find_by_text("Delete report.pdf?")
    assert dialog_title.count == 0

    # Reopen and confirm — wait past the 2s asyncio.sleep in handle_delete.
    open_btn = await flet_app_function.tester.find_by_text("Delete File")
    assert open_btn.count == 1
    await flet_app_function.tester.tap(open_btn)
    await flet_app_function.tester.pump_and_settle()

    delete_btn = await flet_app_function.tester.find_by_text("Delete")
    assert delete_btn.count == 1
    await flet_app_function.tester.tap(delete_btn)
    await flet_app_function.tester.pump_and_settle()

    # Mid-delete state
    deleting_msg = await flet_app_function.tester.find_by_text(
        "Deleting, please wait..."
    )
    assert deleting_msg.count == 1

    # Wait for the async delete (2s) and one pump to let the dialog unmount.
    await asyncio.sleep(2.3)
    await flet_app_function.tester.pump_and_settle()

    dialog_title = await flet_app_function.tester.find_by_text("Delete report.pdf?")
    assert dialog_title.count == 0


# ---------------------------------------------------------------------------
# use_dialog_chained — confirm dialog → success dialog after dismiss
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": use_dialog_chained.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_use_dialog_chained(flet_app_function: ftt.FletTestApp):
    title = await flet_app_function.tester.find_by_text("Chained Dialogs Example")
    assert title.count == 1

    status = await flet_app_function.tester.find_by_text(
        "Click the button to delete the file."
    )
    assert status.count == 1

    # Open confirm dialog
    open_btn = await flet_app_function.tester.find_by_text("Delete File")
    assert open_btn.count == 1
    await flet_app_function.tester.tap(open_btn)
    await flet_app_function.tester.pump_and_settle()

    confirm_title = await flet_app_function.tester.find_by_text("Delete report.pdf?")
    assert confirm_title.count == 1

    # Confirm delete — waits 2s in handle_delete, then closes confirm and
    # (via on_dismiss chaining on the use_ref flag) opens the success dialog.
    # We give the async sleep time to complete *before* pumping again so
    # the dismiss-event round-trip runs inside pump_and_settle.
    delete_btn = await flet_app_function.tester.find_by_text("Delete")
    assert delete_btn.count == 1
    await flet_app_function.tester.tap(delete_btn)

    await asyncio.sleep(2.5)
    await flet_app_function.tester.pump_and_settle()
    # Give the dismiss animation + on_dismiss round-trip one more settle pass.
    await asyncio.sleep(0.3)
    await flet_app_function.tester.pump_and_settle()

    # Success dialog is now up.
    success_title = await flet_app_function.tester.find_by_text("Done!")
    assert success_title.count == 1
    success_body = await flet_app_function.tester.find_by_text(
        "report.pdf has been deleted."
    )
    assert success_body.count == 1

    # Dismiss success dialog via OK.
    ok_btn = await flet_app_function.tester.find_by_text("OK")
    assert ok_btn.count == 1
    await flet_app_function.tester.tap(ok_btn)
    await flet_app_function.tester.pump_and_settle()

    success_title = await flet_app_function.tester.find_by_text("Done!")
    assert success_title.count == 0

    # Status text flipped to "File deleted." and the Delete button is disabled.
    status = await flet_app_function.tester.find_by_text("File deleted.")
    assert status.count == 1


# ---------------------------------------------------------------------------
# use_dialog_multiple — per-item rename and delete dialogs
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": use_dialog_multiple.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_use_dialog_multiple(flet_app_function: ftt.FletTestApp):
    title = await flet_app_function.tester.find_by_text("Multiple Dialogs Example")
    assert title.count == 1

    for name in ("report.pdf", "photo.jpg", "notes.txt"):
        item = await flet_app_function.tester.find_by_text(name)
        assert item.count == 1

    # Open the rename dialog for report.pdf via its pencil tooltip.
    rename_btns = await flet_app_function.tester.find_by_tooltip("Rename")
    assert rename_btns.count == 3
    await flet_app_function.tester.tap(rename_btns.first)
    await flet_app_function.tester.pump_and_settle()

    rename_title = await flet_app_function.tester.find_by_text("Rename report.pdf")
    assert rename_title.count == 1

    cancel_btn = await flet_app_function.tester.find_by_text("Cancel")
    assert cancel_btn.count == 1
    await flet_app_function.tester.tap(cancel_btn)
    await flet_app_function.tester.pump_and_settle()

    rename_title = await flet_app_function.tester.find_by_text("Rename report.pdf")
    assert rename_title.count == 0

    # Open delete dialog for report.pdf — the second file-item row triggers
    # via the Delete tooltip icon.
    delete_btns = await flet_app_function.tester.find_by_tooltip("Delete")
    assert delete_btns.count == 3
    await flet_app_function.tester.tap(delete_btns.first)
    await flet_app_function.tester.pump_and_settle()

    delete_title = await flet_app_function.tester.find_by_text("Delete report.pdf?")
    assert delete_title.count == 1
    body = await flet_app_function.tester.find_by_text("This action cannot be undone.")
    assert body.count == 1

    cancel_btn = await flet_app_function.tester.find_by_text("Cancel")
    assert cancel_btn.count == 1
    await flet_app_function.tester.tap(cancel_btn)
    await flet_app_function.tester.pump_and_settle()

    delete_title = await flet_app_function.tester.find_by_text("Delete report.pdf?")
    assert delete_title.count == 0

    # Confirm a delete on photo.jpg — should remove that row after the 1s
    # simulated async.
    delete_btns = await flet_app_function.tester.find_by_tooltip("Delete")
    assert delete_btns.count == 3
    # tap the second row's delete
    second = delete_btns.at(1)
    await flet_app_function.tester.tap(second)
    await flet_app_function.tester.pump_and_settle()

    delete_title = await flet_app_function.tester.find_by_text("Delete photo.jpg?")
    assert delete_title.count == 1

    confirm = await flet_app_function.tester.find_by_text("Delete")
    assert confirm.count == 1
    await flet_app_function.tester.tap(confirm)
    await flet_app_function.tester.pump_and_settle()

    await asyncio.sleep(1.3)
    await flet_app_function.tester.pump_and_settle()

    delete_title = await flet_app_function.tester.find_by_text("Delete photo.jpg?")
    assert delete_title.count == 0
    photo = await flet_app_function.tester.find_by_text("photo.jpg")
    assert photo.count == 0
    report = await flet_app_function.tester.find_by_text("report.pdf")
    assert report.count == 1
    notes = await flet_app_function.tester.find_by_text("notes.txt")
    assert notes.count == 1

import json
from dataclasses import replace

import pytest
from models import ExpenseDraft
from services.receipts import MAX_WEB_BYTES, ReceiptError
from state import AppState
from storage import PREFIX

PHOTO = b"receipt-bytes"


def draft(**changes):
    return replace(ExpenseDraft("12.50", "Food", "2026-11-10"), **changes)


async def test_photo_is_stored_apart_from_the_ledger(state, storage, photos):
    item = await state.add_expense(draft(receipt_data=PHOTO))

    assert await photos.load(item.receipt_ref) == PHOTO
    saved = json.loads(storage.prefs.values[PREFIX + "data"])["expenses"][0]
    assert saved["receipt_ref"] == item.receipt_ref
    assert "receipt_data" not in saved


def test_oversized_photo_is_rejected(photos):
    with pytest.raises(ReceiptError):
        photos.validate(b"x" * (MAX_WEB_BYTES + 1))


async def test_undo_brings_the_photo_back(state, photos):
    item = await state.add_expense(draft(receipt_data=PHOTO))
    removed = await state.delete_expense(item.id)
    assert await photos.load(item.receipt_ref) == PHOTO  # kept until restart

    await state.restore_expense(removed)
    assert state.expense(item.id).receipt_ref == item.receipt_ref


async def test_unused_photos_are_removed_on_the_next_start(state, storage, photos):
    item = await state.add_expense(draft(receipt_data=PHOTO))
    await state.update_expense(item.id, draft(receipt_ref=None))

    await AppState(storage, photos).load()
    assert await photos.load(item.receipt_ref) is None


async def test_failed_save_leaves_no_photo_behind(state, storage, photos):
    before = set(photos.prefs.values)
    storage.prefs.fail = True
    with pytest.raises(OSError):
        await state.add_expense(draft(receipt_data=PHOTO))
    assert set(photos.prefs.values) == before

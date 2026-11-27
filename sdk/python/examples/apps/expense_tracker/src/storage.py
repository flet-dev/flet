"""The whole ledger is one versioned JSON document in SharedPreferences.

Saving it in one write keeps expenses, categories and the currency consistent.
"""

import json
from dataclasses import asdict

from categories import default_categories
from data import CURRENCIES
from models import Category, Expense, SavedData

import flet as ft

PREFIX = "expense_tracker."
SCHEMA_VERSION = 1


class Storage:
    def __init__(self):
        self.prefs = ft.SharedPreferences()

    async def load_data(self) -> SavedData:
        raw = await self.prefs.get(PREFIX + "data")
        if not raw:
            return SavedData((), default_categories())
        document = json.loads(raw)
        if document["schema_version"] > SCHEMA_VERSION:
            raise ValueError("This data needs a newer version of Expense Tracker.")
        # When the format changes, bump SCHEMA_VERSION and upgrade older documents
        # here. A new field with a dataclass default needs no upgrade.
        currency = document.get("currency", "USD")
        return SavedData(
            tuple(Expense(**item) for item in document["expenses"]),
            tuple(Category(**item) for item in document["categories"]),
            currency if currency in CURRENCIES else "USD",
        )

    async def save_data(self, snapshot: SavedData) -> None:
        document = {"schema_version": SCHEMA_VERSION, **asdict(snapshot)}
        if not await self.prefs.set(PREFIX + "data", json.dumps(document)):
            raise OSError("Device storage could not save your changes.")

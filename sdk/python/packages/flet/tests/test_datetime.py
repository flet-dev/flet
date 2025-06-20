import datetime

import flet as ft


def test_localdate_serialize():
    dt = datetime.datetime(year=2024, month=1, day=20)
    print("\nNaive:", dt.isoformat())
    print("Local:", dt.astimezone().isoformat())
    print("UTC:", dt.astimezone().astimezone(datetime.timezone.utc).isoformat())

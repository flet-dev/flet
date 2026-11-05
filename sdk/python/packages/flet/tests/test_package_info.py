import asyncio
import datetime

import msgpack
import pytest

import flet as ft
from flet.controls.base_control import BaseControl
from flet.messaging.connection import Connection
from flet.messaging.protocol import (
    configure_encode_object_for_msgpack,
    decode_ext_from_msgpack,
)
from flet.messaging.session import Session
from flet.pubsub.pubsub_hub import PubSubHub


class _RecordingConnection(Connection):
    def __init__(self):
        super().__init__()
        self.messages = []

    def send_message(self, message):
        self.messages.append(message)


async def _get_package_info(result):
    """Calls `page.get_package_info()`, answering it with `result`."""
    conn = _RecordingConnection()
    conn.pubsubhub = PubSubHub()
    conn.loop = asyncio.get_running_loop()
    session = Session(conn)
    try:
        call = asyncio.create_task(session.page.get_package_info())
        await asyncio.sleep(0)
        request = conn.messages[-1].body
        assert request.name == "get_package_info"
        session.handle_invoke_method_results(
            session.page._i, request.call_id, result, None
        )
        return await call
    finally:
        session.close()


def _roundtrip(value):
    """Passes `value` through msgpack as the Dart client sends it."""
    return msgpack.unpackb(
        msgpack.packb(
            value,
            default=configure_encode_object_for_msgpack(BaseControl),
        ),
        ext_hook=decode_ext_from_msgpack,
    )


@pytest.mark.asyncio
async def test_get_package_info():
    installed = datetime.datetime(2026, 1, 2, 3, 4, 5, tzinfo=datetime.timezone.utc)
    updated = datetime.datetime(2026, 2, 3, 4, 5, 6, tzinfo=datetime.timezone.utc)

    info = await _get_package_info(
        _roundtrip(
            {
                "app_name": "My App",
                "package_name": "com.mycompany.myapp",
                "version": "1.2.3",
                "build_number": "42",
                "build_signature": "ABCDEF",
                "installer_store": "com.android.vending",
                "install_time": installed,
                "update_time": updated,
            }
        )
    )

    assert info == ft.PackageInfo(
        app_name="My App",
        package_name="com.mycompany.myapp",
        version="1.2.3",
        build_number="42",
        build_signature="ABCDEF",
        installer_store="com.android.vending",
        install_time=installed,
        update_time=updated,
    )


@pytest.mark.asyncio
async def test_get_package_info_unavailable_fields():
    # Web: no installer store or timestamps, and an empty build signature.
    info = await _get_package_info(
        {
            "app_name": "my_app",
            "package_name": "my_app",
            "version": "1.0.0",
            "build_number": "1",
            "build_signature": "",
            "installer_store": None,
            "install_time": None,
            "update_time": None,
        }
    )

    assert info.version == "1.0.0"
    assert info.build_number == "1"
    assert info.build_signature == ""
    assert info.installer_store is None
    assert info.install_time is None
    assert info.update_time is None

"""Tests for the Android post-build patcher."""

import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from flet_notifications.patcher import patch_gradle, patch_manifest

ANDROID_NS = "http://schemas.android.com/apk/res/android"

MANIFEST_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.app">
    <uses-permission android:name="android.permission.INTERNET" />
    <application
        android:label="app"
        android:icon="@mipmap/ic_launcher">
        <activity
            android:name=".MainActivity"
            android:exported="true" />
    </application>
</manifest>
"""

GRADLE_TEMPLATE = """android {
    namespace = "com.example.app"
    defaultConfig {
        applicationId = "com.example.app"
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
    }
    dependencies {}
}
"""


@pytest.fixture
def manifest(tmp_path: Path) -> Path:
    path = tmp_path / "AndroidManifest.xml"
    path.write_text(MANIFEST_TEMPLATE, encoding="utf-8")
    return path


@pytest.fixture
def gradle(tmp_path: Path) -> Path:
    path = tmp_path / "build.gradle.kts"
    path.write_text(GRADLE_TEMPLATE, encoding="utf-8")
    return path


def _root(manifest: Path) -> ET.Element:
    return ET.parse(manifest).getroot()


def _receiver_names(manifest: Path) -> set[str]:
    app = _root(manifest).find("application")
    return {r.get(f"{{{ANDROID_NS}}}name") for r in app.findall("receiver")}


def test_patch_adds_receivers_and_permissions(manifest: Path):
    changed = patch_manifest(manifest)
    receivers = _receiver_names(manifest)
    assert (
        "com.dexterous.flutterlocalnotifications.ActionBroadcastReceiver" in receivers
    )
    assert (
        "com.dexterous.flutterlocalnotifications.ScheduledNotificationReceiver"
        in receivers
    )
    assert (
        "com.dexterous.flutterlocalnotifications.ScheduledNotificationBootReceiver"
        in receivers
    )
    root = _root(manifest)
    perms = {e.get(f"{{{ANDROID_NS}}}name") for e in root.findall("uses-permission")}
    assert "android.permission.POST_NOTIFICATIONS" in perms
    assert "android.permission.RECEIVE_BOOT_COMPLETED" in perms
    assert "android.permission.SCHEDULE_EXACT_ALARM" in perms
    assert "android.permission.INTERNET" in perms  # untouched
    assert len(changed) >= 7


def test_patch_is_idempotent(manifest: Path):
    first = patch_manifest(manifest)
    assert first  # something changed
    snapshot = manifest.read_text(encoding="utf-8")
    second = patch_manifest(manifest)
    assert second == []
    assert manifest.read_text(encoding="utf-8") == snapshot


def test_boot_receiver_gets_intent_filters(manifest: Path):
    patch_manifest(manifest)
    app = _root(manifest).find("application")
    boot = next(
        r
        for r in app.findall("receiver")
        if r.get(f"{{{ANDROID_NS}}}name", "").endswith(
            "ScheduledNotificationBootReceiver"
        )
    )
    actions = {
        e.get(f"{{{ANDROID_NS}}}name")
        for f in boot.findall("intent-filter")
        for e in f.findall("action")
    }
    assert "android.intent.action.BOOT_COMPLETED" in actions
    assert "android.intent.action.QUICKBOOT_POWERON" in actions
    assert boot.get(f"{{{ANDROID_NS}}}exported") == "false"


def test_gradle_patch_enables_desugaring(gradle: Path):
    changed = patch_gradle(gradle)
    text = gradle.read_text(encoding="utf-8")
    assert "isCoreLibraryDesugaringEnabled = true" in text
    assert "desugar_jdk_libs:2.1.4" in text
    assert "multiDexEnabled = true" in text
    assert len(changed) == 3


def test_gradle_patch_is_idempotent(gradle: Path):
    patch_gradle(gradle)
    snapshot = gradle.read_text(encoding="utf-8")
    assert patch_gradle(gradle) == []
    assert gradle.read_text(encoding="utf-8") == snapshot


def test_gradle_patch_missing_file_is_noop(tmp_path: Path):
    assert patch_gradle(tmp_path / "nope.kts") == []


REALISTIC_GRADLE = """android {
    namespace = "com.example.app"
    defaultConfig {
        applicationId = "com.example.app"
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
    }
    dependencies {
        implementation("org.jetbrains.kotlin:kotlin-stdlib:1.9.0")
    }
}
"""

FGS_TYPES = {
    "camera",
    "connectedDevice",
    "dataSync",
    "health",
    "location",
    "mediaPlayback",
    "mediaProjection",
    "microphone",
    "phoneCall",
    "remoteMessaging",
    "shortService",
    "specialUse",
    "systemExempted",
}


def test_gradle_patch_handles_realistic_dependencies_block(tmp_path: Path):
    from flet_notifications.patcher import patch_gradle

    gradle = tmp_path / "build.gradle.kts"
    gradle.write_text(REALISTIC_GRADLE, encoding="utf-8")
    changed = patch_gradle(gradle)
    text = gradle.read_text(encoding="utf-8")
    assert "isCoreLibraryDesugaringEnabled = true" in text
    assert "desugar_jdk_libs:2.1.4" in text
    assert "multiDexEnabled = true" in text
    # The original dependency must survive the insertion.
    assert 'implementation("org.jetbrains.kotlin:kotlin-stdlib:1.9.0")' in text
    assert len(changed) == 3
    # Idempotent on the realistic file too.
    assert patch_gradle(gradle) == []


def test_gradle_patch_no_dependencies_block_reports_nothing(capsys):
    import tempfile

    from flet_notifications.patcher import patch_gradle

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "build.gradle.kts"
        path.write_text('android {\n    namespace = "x"\n}\n', encoding="utf-8")
        changed = patch_gradle(path)
        assert changed == []
        captured = capsys.readouterr()
        assert "warning" in captured.err
        assert "no `dependencies {`" in captured.err


def test_patch_manifest_repairs_incomplete_boot_receiver(tmp_path: Path):
    from flet_notifications.patcher import patch_manifest

    manifest = tmp_path / "AndroidManifest.xml"
    manifest.write_text(
        MANIFEST_TEMPLATE.replace(
            '    <application\n        android:label="app"',
            '''    <application
        android:label="app">
        <receiver
            android:name="com.dexterous.flutterlocalnotifications.ScheduledNotificationBootReceiver"''',
        ),
        encoding="utf-8",
    )
    # simpler: build a manifest with a partial receiver directly
    partial = MANIFEST_TEMPLATE.replace(
        "</application>",
        """<receiver
            android:name="com.dexterous.flutterlocalnotifications.ScheduledNotificationBootReceiver"
            android:exported="false" />
    </application>""",
    )
    manifest.write_text(partial, encoding="utf-8")
    patch_manifest(manifest)
    root = ET.parse(manifest).getroot()
    app = root.find("application")
    boot = next(
        r
        for r in app.findall("receiver")
        if r.get(f"{{{ANDROID_NS}}}name", "").endswith("BootReceiver")
    )
    actions = {
        e.get(f"{{{ANDROID_NS}}}name")
        for f in boot.findall("intent-filter")
        for e in f.findall("action")
    }
    assert "android.intent.action.BOOT_COMPLETED" in actions
    assert "android.intent.action.QUICKBOOT_POWERON" in actions


def test_foreground_service_adds_service_and_permissions(manifest: Path):
    from flet_notifications.patcher import patch_foreground_service

    changed = patch_foreground_service(manifest, "dataSync")
    root = ET.parse(manifest).getroot()
    app = root.find("application")
    service = next(
        s
        for s in app.findall("service")
        if s.get(f"{{{ANDROID_NS}}}name", "").endswith("ForegroundService")
    )
    assert service.get(f"{{{ANDROID_NS}}}foregroundServiceType") == "dataSync"
    perms = {e.get(f"{{{ANDROID_NS}}}name") for e in root.findall("uses-permission")}
    assert "android.permission.FOREGROUND_SERVICE" in perms
    assert "android.permission.FOREGROUND_SERVICE_DATA_SYNC" in perms
    assert changed == ["foreground service (dataSync)"]


def test_foreground_service_rejects_unknown_type(manifest: Path):
    from flet_notifications.patcher import patch_foreground_service

    with pytest.raises(ValueError, match="unknown foreground-service type"):
        patch_foreground_service(manifest, "magic")


def test_foreground_service_is_idempotent(manifest: Path):
    from flet_notifications.patcher import patch_foreground_service

    patch_foreground_service(manifest, "specialUse")
    snapshot = manifest.read_text(encoding="utf-8")
    assert patch_foreground_service(manifest, "specialUse") == []
    assert manifest.read_text(encoding="utf-8") == snapshot

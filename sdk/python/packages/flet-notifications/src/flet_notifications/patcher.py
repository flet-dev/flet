"""Post-build patcher for Flet Android apps using flet-notifications.

`flet build apk` generates the Flutter/Android project but
`[tool.flet.android.*]` can only express permissions, features, meta-data
and providers — not the `<receiver>` entries or the Gradle desugaring
flags that `flutter_local_notifications` needs. This script applies them
to the generated project, idempotently.

Usage::

    uv run flet build apk --yes --project myapp --org com.example -v
    uv run flet-notifications-patch --project-root build/flutter
    cd build/flutter/android && ./gradlew assembleRelease

Options:
    --foreground-service-type TYPE   Opt in to the foreground-service
                                     manifest entry (e.g. `specialUse`).
                                     Without it, only the notification
                                     receivers and permissions are patched.
"""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ANDROID_NS = "http://schemas.android.com/apk/res/android"
NS = {"android": ANDROID_NS}

RECEIVERS = [
    # name, needs_boot_filter
    ("com.dexterous.flutterlocalnotifications.ActionBroadcastReceiver", False),
    ("com.dexterous.flutterlocalnotifications.ScheduledNotificationReceiver", False),
    ("com.dexterous.flutterlocalnotifications.ScheduledNotificationBootReceiver", True),
]

PERMISSIONS = [
    "android.permission.POST_NOTIFICATIONS",
    "android.permission.VIBRATE",
    "android.permission.RECEIVE_BOOT_COMPLETED",
    "android.permission.SCHEDULE_EXACT_ALARM",
]

BOOT_ACTIONS = [
    "android.intent.action.BOOT_COMPLETED",
    "android.intent.action.MY_PACKAGE_REPLACED",
    "android.intent.action.QUICKBOOT_POWERON",
    "com.htc.intent.action.QUICKBOOT_POWERON",
]


def _android_attr(name: str) -> str:
    return f"{{{ANDROID_NS}}}{name}"


def patch_manifest(manifest_path: Path) -> list[str]:
    """Ensure receivers and permissions exist in the app manifest.

    Returns a list of human-readable descriptions of what changed.
    """
    ET.register_namespace("android", ANDROID_NS)
    tree = ET.parse(manifest_path)
    root = tree.getroot()
    changed: list[str] = []

    for permission in PERMISSIONS:
        existing = root.findall(f"uses-permission[@android:name='{permission}']", NS)
        if not existing:
            element = ET.Element("uses-permission")
            element.set(_android_attr("name"), permission)
            root.insert(0, element)
            changed.append(f"permission {permission.split('.')[-1]}")

    application = root.find("application")
    if application is None:
        print(
            f"warning: no <application> in {manifest_path}; skipped receivers",
            file=sys.stderr,
        )
        return changed

    for name, boot_filter in RECEIVERS:
        existing = application.findall(f"receiver[@android:name='{name}']", NS)
        if existing:
            # Repair an incomplete receiver: a boot receiver without its
            # intent-filter set never receives boot events.
            receiver = existing[0]
            if boot_filter and not receiver.findall("intent-filter"):
                for action in BOOT_ACTIONS:
                    intent = ET.SubElement(receiver, "intent-filter")
                    ET.SubElement(intent, "action").set(_android_attr("name"), action)
                changed.append(f"receiver {name.rsplit('.', 1)[-1]} filters")
            if receiver.get(_android_attr("exported")) != "false":
                receiver.set(_android_attr("exported"), "false")
                changed.append(f"receiver {name.rsplit('.', 1)[-1]} exported")
            continue
        receiver = ET.SubElement(application, "receiver")
        receiver.set(_android_attr("name"), name)
        receiver.set(_android_attr("exported"), "false")
        if boot_filter:
            for action in BOOT_ACTIONS:
                intent = ET.SubElement(receiver, "intent-filter")
                ET.SubElement(intent, "action").set(_android_attr("name"), action)
        changed.append(f"receiver {name.rsplit('.', 1)[-1]}")

    if changed:
        tree.write(manifest_path, encoding="utf-8", xml_declaration=True)
    return changed


def patch_gradle(gradle_path: Path) -> list[str]:
    """Enable core-library desugaring (FLN v19+ requirement).

    Real Flet projects have a non-empty `dependencies { ... }` block, so
    the desugaring line is inserted after the opening brace rather than
    matching only the literal empty form. Missing anchors are reported on
    stderr instead of silently succeeding.
    """
    if not gradle_path.exists():
        return []
    text = gradle_path.read_text(encoding="utf-8")
    changed: list[str] = []
    warnings: list[str] = []

    if "isCoreLibraryDesugaringEnabled" not in text:
        if "compileOptions {" in text:
            text = text.replace(
                "compileOptions {",
                "compileOptions {\n        isCoreLibraryDesugaringEnabled = true",
                1,
            )
            changed.append("isCoreLibraryDesugaringEnabled")
        else:
            warnings.append(
                "no `compileOptions {` block found; add "
                "`isCoreLibraryDesugaringEnabled = true` manually"
            )

    if "coreLibraryDesugaring" not in text:
        if "dependencies {" in text:
            text = text.replace(
                "dependencies {",
                "dependencies {\n    "
                'coreLibraryDesugaring("com.android.tools:desugar_jdk_libs:2.1.4")',
                1,
            )
            changed.append("coreLibraryDesugaring")
        else:
            warnings.append(
                "no `dependencies {` block found; add "
                'coreLibraryDesugaring("com.android.tools:desugar_jdk_libs:2.1.4") '
                "manually"
            )

    if "multiDexEnabled" not in text:
        if "defaultConfig {" in text:
            text = text.replace(
                "defaultConfig {",
                "defaultConfig {\n        multiDexEnabled = true",
                1,
            )
            changed.append("multiDexEnabled")
        else:
            warnings.append(
                "no `defaultConfig {` block found; add `multiDexEnabled = true` "
                "manually"
            )

    if changed:
        gradle_path.write_text(text, encoding="utf-8")
    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)
    return changed


# Android 14+ foreground-service types that map to FOREGROUND_SERVICE_*
# permissions (shortService and dataSync-style values map to real
# permissions; everything else must be a known type).
_FGS_TYPES = {
    "camera": "FOREGROUND_SERVICE_CAMERA",
    "connectedDevice": "FOREGROUND_SERVICE_CONNECTED_DEVICE",
    "dataSync": "FOREGROUND_SERVICE_DATA_SYNC",
    "health": "FOREGROUND_SERVICE_HEALTH",
    "location": "FOREGROUND_SERVICE_LOCATION",
    "mediaPlayback": "FOREGROUND_SERVICE_MEDIA_PLAYBACK",
    "mediaProjection": "FOREGROUND_SERVICE_MEDIA_PROJECTION",
    "microphone": "FOREGROUND_SERVICE_MICROPHONE",
    "phoneCall": "FOREGROUND_SERVICE_PHONE_CALL",
    "remoteMessaging": "FOREGROUND_SERVICE_REMOTE_MESSAGING",
    "shortService": "FOREGROUND_SERVICE_SHORT_SERVICE",
    "specialUse": "FOREGROUND_SERVICE_SPECIAL_USE",
    "systemExempted": "FOREGROUND_SERVICE_SYSTEM_EXEMPTED",
}


def patch_foreground_service(manifest_path: Path, service_type: str) -> list[str]:
    """Add the ForegroundService declaration and permissions (opt-in)."""
    if service_type not in _FGS_TYPES:
        raise ValueError(
            f"unknown foreground-service type {service_type!r}; "
            f"expected one of: {', '.join(_FGS_TYPES)}"
        )
    ET.register_namespace("android", ANDROID_NS)
    tree = ET.parse(manifest_path)
    root = tree.getroot()
    application = root.find("application")
    if application is None:
        return []
    service_name = "com.dexterous.flutterlocalnotifications.ForegroundService"
    existing = application.findall(f"service[@android:name='{service_name}']", NS)
    if existing:
        return []
    service = ET.SubElement(application, "service")
    service.set(_android_attr("name"), service_name)
    service.set(_android_attr("exported"), "false")
    service.set(_android_attr("foregroundServiceType"), service_type)
    if service_type == "specialUse":
        # Android 14 requires the subtype property for specialUse.
        prop = ET.SubElement(service, "property")
        prop.set(
            _android_attr("name"),
            "android.app.PROPERTY_SPECIAL_USE_FGS_SUBTYPE",
        )
        prop.set(
            _android_attr("value"),
            "flet-notifications foreground service",
        )
    for permission in (
        "android.permission.FOREGROUND_SERVICE",
        f"android.permission.{_FGS_TYPES[service_type]}",
    ):
        if not root.findall(f"uses-permission[@android:name='{permission}']", NS):
            element = ET.Element("uses-permission")
            element.set(_android_attr("name"), permission)
            root.insert(0, element)
    tree.write(manifest_path, encoding="utf-8", xml_declaration=True)
    return [f"foreground service ({service_type})"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="flet-notifications-patch",
        description="Patch a generated Flet Android project for "
        "flet-notifications (receivers, permissions, desugaring).",
    )
    parser.add_argument(
        "--project-root",
        default="build/flutter",
        help="Path to the generated Flutter project (default: build/flutter)",
    )
    parser.add_argument(
        "--foreground-service-type",
        default=None,
        help="Opt in to the ForegroundService manifest entry with this "
        "type (e.g. specialUse). Omit to skip foreground-service setup.",
    )
    args = parser.parse_args(argv)

    project = Path(args.project_root)
    manifest = project / "android" / "app" / "src" / "main" / "AndroidManifest.xml"
    gradle = project / "android" / "app" / "build.gradle.kts"

    if not manifest.exists():
        print(f"error: manifest not found: {manifest}", file=sys.stderr)
        return 1

    changes = patch_manifest(manifest)
    changes += patch_gradle(gradle)
    if args.foreground_service_type:
        changes += patch_foreground_service(manifest, args.foreground_service_type)

    if changes:
        print("flet-notifications-patch applied:")
        for change in changes:
            print(f"  + {change}")
    else:
        print("flet-notifications-patch: nothing to do (already patched)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Helpers for Android-specific build configuration."""

import re

ANDROID_ARCH_TO_FLUTTER_TARGET_PLATFORM = {
    "armeabi-v7a": "android-arm",
    "arm64-v8a": "android-arm64",
    "x86_64": "android-x64",
}
"""Android ABIs supported by Flutter, mapped to `flutter build --target-platform`
values. Order is meaningful: it defines the order in which
generated artifacts (e.g. Gradle packaging excludes) list ABIs."""


def flutter_target_platforms(archs: list[str]) -> list[str]:
    """
    Map Android ABI names to `flutter build --target-platform` values.

    Args:
        archs: Android ABI names, e.g. `["arm64-v8a"]`.

    Returns:
        The corresponding Flutter target platforms, e.g. `["android-arm64"]`.

    Raises:
        ValueError: If any ABI is not supported by Flutter.
    """

    platforms = []
    for arch in archs:
        platform = ANDROID_ARCH_TO_FLUTTER_TARGET_PLATFORM.get(arch)
        if platform is None:
            raise ValueError(
                f"Unsupported Android architecture: {arch!r}. "
                f"Supported: {', '.join(ANDROID_ARCH_TO_FLUTTER_TARGET_PLATFORM)}."
            )
        platforms.append(platform)
    return platforms


def excluded_android_abis(archs: list[str]) -> list[str]:
    """
    Return the supported Android ABIs not requested in `archs`.

    Args:
        archs: Requested Android ABI names; an empty list means "all ABIs"
            and yields no exclusions.

    Returns:
        ABIs to exclude from the generated artifact.
    """

    if not archs:
        return []
    return [abi for abi in ANDROID_ARCH_TO_FLUTTER_TARGET_PLATFORM if abi not in archs]


def normalize_android_receivers(configured) -> dict:
    """Validate receiver tables and normalize their manifest attributes.

    Raises:
        ValueError: If a receiver declaration or intent filter is malformed.
    """
    setting = "tool.flet.android.receiver"

    def fail(path, message):
        raise ValueError(f"Invalid {path}: {message}.")

    if configured is None:
        return {}
    if not isinstance(configured, dict):
        fail(setting, "expected a table of receivers")

    resolved = {}
    for name, receiver in configured.items():
        path = f'{setting}."{name}"'
        if not isinstance(name, str) or not name.strip():
            fail(setting, "expected a nonempty receiver class name")
        if receiver is False or receiver == {}:
            continue
        if not isinstance(receiver, dict):
            fail(path, "expected an attribute table or false")

        attributes = {}
        for key, value in receiver.items():
            if key == "intent_filter":
                continue
            if key == "name":
                fail(f"{path}.name", "name is reserved for the receiver table key")
            if not isinstance(key, str) or not re.fullmatch(
                r"[A-Za-z_][A-Za-z0-9_]*", key
            ):
                fail(path, f"invalid Android attribute name {key!r}")
            if not isinstance(value, (str, bool, int, float)):
                fail(f"{path}.{key}", "expected a string, boolean, or number")
            attributes[key] = (
                str(value).lower() if isinstance(value, bool) else str(value)
            )

        filters = receiver.get("intent_filter", [])
        if not isinstance(filters, list):
            fail(f"{path}.intent_filter", "expected a list of filter tables")
        normalized_filters = []
        for index, intent_filter in enumerate(filters):
            filter_path = f"{path}.intent_filter[{index}]"
            if not isinstance(intent_filter, dict):
                fail(filter_path, "expected a filter table")
            for key in intent_filter:
                if key not in ("actions", "categories"):
                    fail(
                        f"{filter_path}.{key}",
                        "only actions and categories are supported",
                    )
            normalized = {}
            for key in ("actions", "categories"):
                values = intent_filter.get(key, [])
                if not isinstance(values, list):
                    fail(f"{filter_path}.{key}", "expected a list of nonempty strings")
                for value in values:
                    if not isinstance(value, str) or not value.strip():
                        fail(
                            f"{filter_path}.{key}",
                            "expected a list of nonempty strings",
                        )
                normalized[key] = values.copy()
            if not normalized["actions"]:
                fail(f"{filter_path}.actions", "at least one action is required")
            normalized_filters.append(normalized)

        if normalized_filters and "exported" not in attributes:
            fail(
                f"{path}.exported", "an explicit value is required with intent filters"
            )
        resolved[name] = {
            "attributes": attributes,
            "intent_filters": normalized_filters,
        }
    return resolved


def normalize_android_services(configured) -> dict:
    """Validate service attributes and nested property and metadata declarations.

    Raises:
        ValueError: If a service or one of its child declarations is malformed.
    """
    setting = "tool.flet.android.service"

    def fail(path, message):
        """Report a malformed declaration using its full configuration path."""
        raise ValueError(f"Invalid {path}: {message}.")

    def attributes(values, path):
        """Validate attribute names and normalize scalar values for XML."""
        resolved = {}
        for key, value in values.items():
            if key == "name":
                fail(f"{path}.name", "name is reserved for the table key")
            if not isinstance(key, str) or not re.fullmatch(
                r"[A-Za-z_][A-Za-z0-9_]*", key
            ):
                fail(path, f"invalid Android attribute name {key!r}")
            if not isinstance(value, (str, bool, int, float)):
                fail(f"{path}.{key}", "expected a string, boolean, or number")
            resolved[key] = (
                str(value).lower() if isinstance(value, bool) else str(value)
            )
        return resolved

    if configured is None:
        return {}
    if not isinstance(configured, dict):
        fail(setting, "expected a table of services")

    resolved = {}
    for name, service in configured.items():
        path = f'{setting}."{name}"'
        if not isinstance(name, str) or not name.strip():
            fail(setting, "expected a nonempty service class name")
        if service is False or service == {}:
            continue
        if not isinstance(service, dict):
            fail(path, "expected an attribute table or false")
        entry = {
            "attributes": attributes(
                {
                    k: v
                    for k, v in service.items()
                    if k not in ("property", "meta_data")
                },
                path,
            )
        }
        for kind in ("property", "meta_data"):
            children = service.get(kind, {})
            if not isinstance(children, dict):
                fail(f"{path}.{kind}", "expected a table of named declarations")
            normalized = {}
            for child_name, child in children.items():
                child_path = f'{path}.{kind}."{child_name}"'
                if not isinstance(child_name, str) or not child_name.strip():
                    fail(f"{path}.{kind}", "expected a nonempty declaration name")
                child_attributes = attributes(
                    child if isinstance(child, dict) else {"value": child}, child_path
                )
                if set(child_attributes) not in ({"value"}, {"resource"}):
                    fail(child_path, "specify exactly one of value or resource")
                if "resource" in child_attributes and (
                    not isinstance(child["resource"], str)
                    or not child["resource"].strip()
                ):
                    fail(
                        f"{child_path}.resource", "expected a nonempty resource string"
                    )
                normalized[child_name] = child_attributes
            entry[kind] = normalized
        resolved[name] = entry
    return resolved

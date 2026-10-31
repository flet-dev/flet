"""Helpers for Android-specific build configuration."""

import re
from pathlib import Path
from typing import Optional

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


def _android_attributes(values: dict, path: str, reserved=()) -> dict:
    """Validate Android attribute names and normalize scalar values for XML.

    Raises:
        ValueError: If a name is not an attribute name or a value isn't a string,
            boolean, or number.
    """
    resolved = {}
    for key, value in values.items():
        if key in reserved:
            continue
        if not isinstance(key, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key):
            raise ValueError(f"Invalid {path}: invalid Android attribute name {key!r}.")
        if not isinstance(value, (str, bool, int, float)):
            raise ValueError(
                f"Invalid {path}.{key}: expected a string, boolean, or number."
            )
        resolved[key] = str(value).lower() if isinstance(value, bool) else str(value)
    return resolved


def normalize_android_intent_filters(filters, path: str) -> list:
    """Validate a list of `<intent-filter>` tables.

    Each table needs at least one action in `actions` and may have
    `categories` and `data`: a table, or list of tables, of `<data>`
    attributes. Its other entries become the filter's own attributes, such as
    `autoVerify` or `priority`.

    Args:
        filters: The configured list of filter tables.
        path: The setting's path, used in error messages.

    Returns:
        Each filter's `attributes`, `actions`, `categories` and `data` list.

    Raises:
        ValueError: If a filter is malformed.
    """

    def fail(at, message):
        """Report a malformed filter using its full configuration path."""
        raise ValueError(f"Invalid {at}: {message}.")

    if not isinstance(filters, list):
        fail(path, "expected a list of filter tables")
    normalized_filters = []
    for index, intent_filter in enumerate(filters):
        filter_path = f"{path}[{index}]"
        if not isinstance(intent_filter, dict):
            fail(filter_path, "expected a filter table")
        for key in ("action", "category"):
            if key in intent_filter:
                fail(f"{filter_path}.{key}", f"use {key}s, a list of names")
        normalized = {
            "attributes": _android_attributes(
                intent_filter, filter_path, ("actions", "categories", "data")
            )
        }
        for key in ("actions", "categories"):
            values = intent_filter.get(key, [])
            if not isinstance(values, list) or not all(
                isinstance(value, str) and value.strip() for value in values
            ):
                fail(f"{filter_path}.{key}", "expected a list of nonempty strings")
            normalized[key] = [value.strip() for value in values]
        if not normalized["actions"]:
            fail(f"{filter_path}.actions", "at least one action is required")
        data = intent_filter.get("data", [])
        single = isinstance(data, dict)
        if not isinstance(data, (dict, list)):
            fail(
                f"{filter_path}.data", "expected a data table or a list of data tables"
            )
        normalized["data"] = []
        for data_index, element in enumerate([data] if single else data):
            data_path = (
                f"{filter_path}.data" if single else f"{filter_path}.data[{data_index}]"
            )
            if not isinstance(element, dict) or not element:
                fail(data_path, "expected a nonempty table of data attributes")
            normalized["data"].append(_android_attributes(element, data_path))
        normalized_filters.append(normalized)
    return normalized_filters


def normalize_android_activity(configured) -> dict:
    """Validate what the app adds to its main activity.

    Only intent filters are supported; they are added after the activity's own
    launcher and deep-linking filters.

    Returns:
        A table with the activity's `intent_filters`, empty by default.

    Raises:
        ValueError: If the table or one of its filters is malformed.
    """
    setting = "tool.flet.android.activity"
    if configured is None:
        return {"intent_filters": []}
    if not isinstance(configured, dict):
        raise ValueError(f"Invalid {setting}: expected a table.")
    for key in configured:
        if key != "intent_filter":
            raise ValueError(
                f"Invalid {setting}.{key}: only intent_filter is supported."
            )
    return {
        "intent_filters": normalize_android_intent_filters(
            configured.get("intent_filter", []), f"{setting}.intent_filter"
        )
    }


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

        normalized_filters = normalize_android_intent_filters(
            receiver.get("intent_filter", []), f"{path}.intent_filter"
        )

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


def normalize_android_application_attributes(configured, product_name: str) -> dict:
    """Merge the app's `<application>` attributes over the ones Flet sets.

    Flet sets `label` to the product name, `name` to Flutter's application
    class, `enableOnBackInvokedCallback` to `true` and `icon` to the launcher
    icon. An entry with the same key replaces Flet's value instead of adding
    the attribute a second time.

    Args:
        configured: The app's `<application>` attributes, if any.
        product_name: The app's product name, used as the default label.

    Returns:
        Attribute names mapped to their manifest values; booleans are written
            as lowercase `true` or `false`.

    Raises:
        ValueError: If the table, an attribute name or a value is malformed.
    """
    setting = "tool.flet.android.manifest_application"
    resolved = {
        "label": product_name,
        "name": "${applicationName}",
        "enableOnBackInvokedCallback": "true",
        "icon": "@mipmap/ic_launcher",
    }
    if configured is None:
        return resolved
    if not isinstance(configured, dict):
        raise ValueError(f"Invalid {setting}: expected a table of attributes.")
    for key, value in configured.items():
        if not isinstance(key, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key):
            raise ValueError(
                f"Invalid {setting}: invalid Android attribute name {key!r}."
            )
        if not isinstance(value, (str, bool, int, float)):
            raise ValueError(
                f"Invalid {setting}.{key}: expected a string, boolean, or number."
            )
        resolved[key] = str(value).lower() if isinstance(value, bool) else str(value)
    return resolved


ANDROID_QUERIES_DATA_ATTRIBUTES = ("scheme", "host", "mimeType")
"""`<data>` attributes Android supports in a `<queries>` intent; each may be set
once per intent."""


def normalize_android_queries(configured) -> dict:
    """Validate the apps, intents, and providers an app declares it queries.

    Android 11 and later hide other apps from an app unless its manifest names
    them in `<queries>`. Intents follow Android's limits for `<queries>`: one
    action, optional categories, and `<data>` elements that set each of
    `scheme`, `host`, and `mimeType` at most once in total. Duplicate packages
    and providers are dropped.

    Returns:
        A table with `packages`, `intents`, and `providers` lists, empty by default.

    Raises:
        ValueError: If a query declaration is malformed.
    """
    setting = "tool.flet.android.queries"

    def fail(path, message):
        """Report a malformed declaration using its full configuration path."""
        raise ValueError(f"Invalid {path}: {message}.")

    def names(key, pattern, description):
        """Validate a list of names and drop duplicates, keeping their order."""
        values = configured.get(key, [])
        if not isinstance(values, list) or not all(
            isinstance(value, str) and re.fullmatch(pattern, value.strip())
            for value in values
        ):
            fail(f"{setting}.{key}", f"expected a list of {description}")
        return list(dict.fromkeys(value.strip() for value in values))

    resolved = {"packages": [], "intents": [], "providers": []}
    if configured is None:
        return resolved
    if not isinstance(configured, dict):
        fail(setting, "expected a table with packages, intent, or providers")
    for key in configured:
        if key not in ("packages", "intent", "providers"):
            fail(
                f"{setting}.{key}", "only packages, intent, and providers are supported"
            )

    resolved["packages"] = names(
        "packages",
        r"[A-Za-z][A-Za-z0-9_]*(\.[A-Za-z][A-Za-z0-9_]*)+",
        "package names, such as com.example.app",
    )
    resolved["providers"] = names(
        "providers", r"[^\s;]+(;[^\s;]+)*", "provider authorities"
    )

    intents = configured.get("intent", [])
    if not isinstance(intents, list):
        fail(f"{setting}.intent", "expected a list of intent tables")
    for index, intent in enumerate(intents):
        path = f"{setting}.intent[{index}]"
        if not isinstance(intent, dict):
            fail(path, "expected an intent table")
        for key in intent:
            if key not in ("action", "categories", "data"):
                fail(f"{path}.{key}", "only action, categories, and data are supported")
        action = intent.get("action")
        if not isinstance(action, str) or not action.strip():
            fail(f"{path}.action", "expected one nonempty action name")
        categories = intent.get("categories", [])
        if not isinstance(categories, list) or not all(
            isinstance(c, str) and c.strip() for c in categories
        ):
            fail(f"{path}.categories", "expected a list of nonempty strings")
        data = intent.get("data", [])
        single = isinstance(data, dict)
        if single:
            data = [data]
        if not isinstance(data, list):
            fail(f"{path}.data", "expected a data table or a list of data tables")
        normalized_data = []
        used = set()
        for data_index, element in enumerate(data):
            data_path = f"{path}.data" if single else f"{path}.data[{data_index}]"
            if not isinstance(element, dict) or not element:
                fail(data_path, "expected a nonempty table of data attributes")
            for key, value in element.items():
                if key not in ANDROID_QUERIES_DATA_ATTRIBUTES:
                    fail(
                        f"{data_path}.{key}",
                        "only scheme, host, and mimeType are supported in queries",
                    )
                if key in used:
                    fail(f"{data_path}.{key}", f"{key} can be set only once per intent")
                if not isinstance(value, str) or not value.strip():
                    fail(f"{data_path}.{key}", "expected a nonempty string")
                used.add(key)
            normalized_data.append({k: v.strip() for k, v in element.items()})
        resolved["intents"].append(
            {
                "action": action.strip(),
                "categories": [c.strip() for c in categories],
                "data": normalized_data,
            }
        )
    return resolved


ANDROID_RESOURCE_TYPES = {
    "anim",
    "animator",
    "color",
    "drawable",
    "font",
    "interpolator",
    "layout",
    "menu",
    "mipmap",
    "raw",
    "transition",
    "values",
    "xml",
}
"""Android resource directory types an app may supply, before any qualifiers."""

ANDROID_RESOURCES_KEEP_FILE = Path("raw") / "flet_res_keep.xml"
"""Generated keep rule, relative to the project's `res` directory."""


def android_resource_files(res_dir: Path) -> list[Path]:
    """
    List an app's Android resource files and validate their layout.

    The directory mirrors Android's `res` directory: one level of type
    directories, such as `drawable-hdpi` or `raw`, each holding resource files.

    Args:
        res_dir: The app's resource directory.

    Returns:
        Resource file paths relative to `res_dir`, sorted.

    Raises:
        ValueError: If an entry does not follow Android's resource layout or
            naming rules.
    """

    files = []
    seen = {}
    for entry in sorted(res_dir.iterdir()):
        if entry.name.startswith("."):
            continue
        if not entry.is_dir():
            raise ValueError(
                f"{entry}: expected a resource type directory, such as "
                "`drawable` or `raw`."
            )
        if entry.name.split("-")[0] not in ANDROID_RESOURCE_TYPES:
            raise ValueError(
                f"{entry}: unknown Android resource type "
                f"{entry.name.split('-')[0]!r}. Supported: "
                f"{', '.join(sorted(ANDROID_RESOURCE_TYPES))}."
            )
        for file in sorted(entry.iterdir()):
            if file.name.startswith("."):
                continue
            if not file.is_file():
                raise ValueError(f"{file}: resource directories cannot be nested.")
            if not re.fullmatch(r"[a-z][a-z0-9_]*(\.[A-Za-z0-9.]+)?", file.name):
                raise ValueError(
                    f"{file}: Android resource file names may contain only "
                    "lowercase letters, digits, and underscores, and must start "
                    "with a letter."
                )
            relative = file.relative_to(res_dir)
            duplicate = seen.setdefault(
                (entry.name, android_resource_key(relative)), file
            )
            if duplicate != file:
                raise ValueError(
                    f"{file}: defines the same resource as {duplicate.name}."
                )
            files.append(relative)
    return files


def android_resource_key(path: Path) -> tuple[str, str]:
    """
    Identify the resource a file in a `res` directory defines.

    Files define the same resource when they share a resource type and name, even
    in different qualifier directories or with different extensions:
    `drawable-hdpi/splash.png` and `drawable/splash.xml` are both the drawable
    `splash`. Values files merge their contents instead, so they are identified by
    their directory and file name.

    Args:
        path: File path relative to the `res` directory.

    Returns:
        The resource type, or values directory, and the resource or file name.
    """

    kind = path.parent.name.split("-")[0]
    if kind == "values":
        return path.parent.name, path.name
    return kind, path.name.split(".")[0]


def android_resource_clashes(
    files: list[Path], res_path: Path
) -> list[tuple[Path, Path]]:
    """
    Find app resources that would add to or replace resources Flet generates.

    Args:
        files: The app's resource file paths, relative to its resource directory.
        res_path: The generated project's `res` directory, holding only the files
            Flet generates.

    Returns:
        Each clashing app file paired with a generated file defining the same
        resource, both relative to their `res` directories.
    """

    generated = {
        android_resource_key(ANDROID_RESOURCES_KEEP_FILE): ANDROID_RESOURCES_KEEP_FILE
    }
    for path in sorted(res_path.glob("*/*")):
        if path.is_file():
            relative = path.relative_to(res_path)
            generated.setdefault(android_resource_key(relative), relative)
    return [
        (file, generated[android_resource_key(file)])
        for file in files
        if android_resource_key(file) in generated
    ]


def android_resources_keep_xml(files: list[Path]) -> Optional[str]:
    """
    Build a keep rule for resources the app refers to only by name.

    Release builds remove resources that no code references directly, which
    includes resources Python code names at runtime, such as a notification
    icon. Values resources are not file-based and are not listed.

    Args:
        files: Resource file paths relative to the `res` directory.

    Returns:
        The keep file's XML, or `None` when there is nothing to keep.
    """

    names = sorted(
        {
            f"@{file.parent.name.split('-')[0]}/{file.name.split('.')[0]}"
            for file in files
            if file.parent.name.split("-")[0] != "values"
        }
    )
    if not names:
        return None
    return (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<resources xmlns:tools="http://schemas.android.com/tools"\n'
        f'    tools:keep="{",".join(names)}" />\n'
    )

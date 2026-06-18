"""Helpers for Android-specific build configuration."""

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

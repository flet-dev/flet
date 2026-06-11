"""Tests for android utils module."""

import pytest

from flet_cli.utils.android import (
    ANDROID_ARCH_TO_FLUTTER_TARGET_PLATFORM,
    excluded_android_abis,
    flutter_target_platforms,
)

# ---------------------------------------------------------------------------
# flutter_target_platforms
# ---------------------------------------------------------------------------


class TestFlutterTargetPlatforms:
    def test_single_arch(self):
        assert flutter_target_platforms(["arm64-v8a"]) == ["android-arm64"]

    def test_all_archs(self):
        assert flutter_target_platforms(["armeabi-v7a", "arm64-v8a", "x86_64"]) == [
            "android-arm",
            "android-arm64",
            "android-x64",
        ]

    def test_preserves_request_order(self):
        assert flutter_target_platforms(["x86_64", "arm64-v8a"]) == [
            "android-x64",
            "android-arm64",
        ]

    def test_empty(self):
        assert flutter_target_platforms([]) == []

    def test_x86_unsupported(self):
        # serious_python supports x86, but Flutter removed it.
        with pytest.raises(ValueError, match="x86"):
            flutter_target_platforms(["x86"])

    def test_macos_style_arch_rejected(self):
        with pytest.raises(ValueError, match="arm64"):
            flutter_target_platforms(["arm64"])

    def test_error_lists_supported_values(self):
        with pytest.raises(ValueError, match="arm64-v8a"):
            flutter_target_platforms(["bogus"])


# ---------------------------------------------------------------------------
# excluded_android_abis
# ---------------------------------------------------------------------------


class TestExcludedAndroidAbis:
    def test_single_arch(self):
        assert excluded_android_abis(["arm64-v8a"]) == ["armeabi-v7a", "x86_64"]

    def test_two_archs(self):
        assert excluded_android_abis(["arm64-v8a", "x86_64"]) == ["armeabi-v7a"]

    def test_all_archs(self):
        assert (
            excluded_android_abis(list(ANDROID_ARCH_TO_FLUTTER_TARGET_PLATFORM)) == []
        )

    def test_empty_means_no_exclusions(self):
        assert excluded_android_abis([]) == []

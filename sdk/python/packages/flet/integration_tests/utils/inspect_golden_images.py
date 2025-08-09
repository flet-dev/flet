"""
Script to check for mismatches between integration test functions and golden images.

- Scans test files for test functions that use assert_control_screenshot.
- Scans golden image folders for available images.
- Reports missing golden images for tests and golden images without tests, per platform.
- Handles singular/plural mismatches between test file names and golden image folders.
"""

import re
from enum import Enum
from pathlib import Path

# Directory paths for tests and golden images
TESTS_DIR = Path("../controls")
GOLDEN_DIR = Path("../controls/golden")


class Platform(Enum):
    """Supported platforms."""

    MACOS = "macos"
    IOS = "ios"


def get_test_golden_names():
    """
    Scans test files in TESTS_DIR and identifies test functions that use
    `assert_control_screenshot`. Organizes these test functions by base names.

    Returns:
        dict: A dictionary mapping the base name (control type) to a
            set of test function names.
    """
    test_golden = {}

    # Loop through all test files in the TESTS_DIR directory
    for test_file in TESTS_DIR.glob("test_*.py"):
        base_name = test_file.stem.replace(
            "test_", ""
        )  # Extract base name without "test_" prefix

        test_golden.setdefault(base_name, set())  # Ensure key exists for the base name

        with open(test_file) as f:
            content = f.read()
            # Find all async test functions in the test file
            for match in re.finditer(r"async def (test_[^(]+)\(", content):
                test_func = match.group(1)
                func_block = re.search(
                    rf"async def {test_func}.*?(?=async def|$)",
                    content,
                    re.DOTALL,
                )
                # Check if the function contains `assert_control_screenshot`
                if func_block and "assert_control_screenshot" in func_block.group(0):
                    test_golden[base_name].add(test_func.removeprefix("test_"))
    return test_golden


def get_golden_images(platforms: list[Platform]):
    """
    Scans the golden image folders for each platform and returns a mapping of
    golden images organized by platform and control type.

    Args:
        platforms: List of platforms (e.g., [Platform.MACOS, Platform.IOS]) to check.

    Returns:
        dict: A nested dictionary with platform -> control_type ->
            set of golden image names (without extension).
    """
    golden_images = {}
    for platform in platforms:
        plat_dir = GOLDEN_DIR / platform.value
        for control_type_dir in plat_dir.iterdir():
            if not control_type_dir.is_dir():
                continue  # Skip non-directory files
            control_type = control_type_dir.name
            golden_images.setdefault(platform, {}).setdefault(control_type, set())
            # Add image names (without extension) to the set of golden images
            for img in control_type_dir.glob("*.png"):
                golden_images[platform][control_type].add(img.stem)
    return golden_images


def main(
    platforms: list[Platform],
    show_passes: bool = False,
):
    """
    Main function to check for mismatches between test functions and golden images.
    It will report missing golden images, orphan golden images, and optionally
    show matching tests and golden images.

    Args:
        platforms: A list of platforms to check (default is all platforms).
        show_passes: Whether to show tests that have matching golden images.
    """
    # Get mappings of test functions and golden images
    test_golden = get_test_golden_names()
    golden_images = get_golden_images(platforms)

    # Loop through each platform to report mismatches
    for platform in platforms:
        print(f"\nPlatform: {platform}")
        platform_golden = golden_images.get(platform, {})
        all_control_types = set(platform_golden.keys()) | set(test_golden.keys())

        missing = {}
        orphan = {}

        # Check for missing and orphaned golden images for each control type
        for control_type in sorted(all_control_types):
            test_names = test_golden.get(control_type, set())
            golden_names = platform_golden.get(control_type, set())

            # Tests without corresponding golden image
            missing_golden = test_names - golden_names
            # Golden images without corresponding test
            orphan_golden = golden_names - test_names

            if missing_golden:
                missing[control_type] = sorted(missing_golden)
            if orphan_golden:
                orphan[control_type] = sorted(orphan_golden)

        # Report missing golden images
        if missing:
            print("  Missing golden images for tests:")
            for control_type, items in missing.items():
                print(f"    {control_type}: {items}")

        # Report orphan golden images
        if orphan:
            print("  Orphan golden images without tests:")
            for control_type, items in orphan.items():
                print(f"    {control_type}: {[f'{i}.png' for i in items]}")

        # Optionally show matching test-golden pairs
        if show_passes:
            for control_type in sorted(all_control_types):
                test_names = test_golden.get(control_type, set())
                golden_names = platform_golden.get(control_type, set())
                if not (test_names - golden_names) and not (golden_names - test_names):
                    print(f"    {control_type}: All tests and golden images match.")


if __name__ == "__main__":
    main(list(Platform))

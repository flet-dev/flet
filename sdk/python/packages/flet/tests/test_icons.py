import flet as ft


def test_material_icons_random_with_weights_and_exclude():
    """Test random material icon selection with weights and exclusion list."""
    results = [
        ft.Icons.random(
            exclude=[ft.Icons.FAVORITE],
            weights={ft.Icons.SCHOOL: 150},
        )
        for _ in range(1000)
    ]
    assert ft.Icons.FAVORITE not in results
    assert ft.Icons.SCHOOL in results


def test_cupertino_icons_random_with_weights_and_exclude():
    """Test random cupertino icon selection with weights and exclusion list."""
    results = [
        ft.CupertinoIcons.random(
            exclude=[ft.CupertinoIcons.CAMERA_CIRCLE],
            weights={ft.CupertinoIcons.TABLE: 150},
        )
        for _ in range(1000)
    ]
    assert ft.CupertinoIcons.CAMERA_CIRCLE not in results
    assert ft.CupertinoIcons.TABLE in results

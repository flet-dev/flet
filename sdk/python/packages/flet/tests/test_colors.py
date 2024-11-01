import flet as ft


def test_material_colors_random_with_weights_and_exclude():
    """Test random material color selection with weights and exclusion list."""
    results = [
        ft.Colors.random(
            exclude=[ft.Colors.RED],
            weights={ft.Colors.BLUE: 150},
        )
        for _ in range(1000)
    ]
    assert ft.Colors.RED not in results
    assert ft.Colors.BLUE in results


def test_cupertino_colors_random_with_weights_and_exclude():
    """Test random cupertino color selection with weights and exclusion list."""
    results = [
        ft.CupertinoColors.random(
            exclude=[ft.CupertinoColors.SYSTEM_RED],
            weights={ft.CupertinoColors.SEPARATOR: 150},
        )
        for _ in range(1000)
    ]
    assert ft.CupertinoColors.SYSTEM_RED not in results
    assert ft.CupertinoColors.SEPARATOR in results

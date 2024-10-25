import flet_core as ft


def test_material_icons_random_with_weights_and_exclude():
    """Test random material icon selection with weights and exclusion list."""
    results = [
        ft.MaterialIcons.random(
            exclude=[ft.MaterialIcons.FAVORITE],
            weights={ft.MaterialIcons.SCHOOL: 150},
        )
        for _ in range(1000)
    ]
    assert ft.MaterialIcons.FAVORITE not in results
    assert ft.MaterialIcons.SCHOOL in results


def test_cupertino_icons_random_with_weights_and_exclude():
    """Test random cupertino icon selection with weights and exclusion list."""
    results = [
        ft.CupertinoIcons.random(
            exclude=[ft.CupertinoIcons.CAMERA],
            weights={ft.CupertinoIcons.TABLE: 150},
        )
        for _ in range(1000)
    ]
    assert ft.CupertinoIcons.CAMERA not in results
    assert ft.CupertinoIcons.TABLE in results

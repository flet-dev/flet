import flet_core as ft


def run_common_tests(icon_class):
    icon_list = list(icon_class)

    def test_random_no_exclude_no_weights():
        """Test random selection with no exclusion or weights."""
        result = icon_class.random()
        assert result in icon_list

    def test_random_with_exclude():
        """Test random selection with exclusion list."""
        exclude = [icon_list[0], icon_list[1]]
        result = icon_class.random(exclude=exclude)
        assert result in icon_list
        assert result not in exclude

    def test_random_with_exclude_all():
        """Test random selection with exclusion of all elements."""
        exclude = icon_list
        result = icon_class.random(exclude=exclude)
        assert result is None

    def test_random_with_weights():
        """Test random selection with weights."""
        weights = {icon_list[0]: 10}
        results = [icon_class.random(weights=weights) for _ in range(1000)]
        max_count = max(results.count(icon) for icon in icon_class)
        # weighted icon appears most frequently
        assert results.count(icon_list[0]) == max_count

    def test_random_with_weights_and_exclude():
        """Test random selection with weights and exclusion list."""
        exclude = [icon_list[0]]
        weights = {icon: 1 for icon in icon_class}
        results = [
            icon_class.random(exclude=exclude, weights=weights) for _ in range(1000)
        ]
        assert icon_list[0] not in results
        assert icon_list[1] in results

    return [
        test_random_no_exclude_no_weights,
        test_random_with_exclude,
        test_random_with_exclude_all,
        test_random_with_weights,
        test_random_with_weights_and_exclude,
    ]


def test_cupertino_icons():
    for test in run_common_tests(ft.CupertinoIcons):
        test()


def test_material_icons():
    for test in run_common_tests(ft.MaterialIcons):
        test()

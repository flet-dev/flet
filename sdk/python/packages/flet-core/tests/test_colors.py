import flet_core as ft


def run_common_tests(color_class):
    color_list = list(color_class)

    def test_random_no_exclude_no_weights():
        """Test random selection with no exclusion or weights."""
        result = color_class.random()
        assert result in color_list

    def test_random_with_exclude():
        """Test random selection with exclusion list."""
        exclude = [color_list[0], color_list[1]]
        result = color_class.random(exclude=exclude)
        assert result in color_list
        assert result not in exclude

    def test_random_with_exclude_all():
        """Test random selection with exclusion of all elements."""
        exclude = color_list
        result = color_class.random(exclude=exclude)
        assert result is None

    def test_random_with_weights():
        """Test random selection with weights."""
        weights = {color_list[0]: 10}
        results = [color_class.random(weights=weights) for _ in range(1000)]
        max_count = max(results.count(color) for color in color_class)
        # weighted color appears most frequently
        assert results.count(color_list[0]) == max_count

    def test_random_with_weights_and_exclude():
        """Test random selection with weights and exclusion list."""
        exclude = [color_list[0]]
        weights = {color: 1 for color in color_class}
        results = [
            color_class.random(exclude=exclude, weights=weights) for _ in range(1000)
        ]
        assert color_list[0] not in results
        assert color_list[1] in results

    return [
        test_random_no_exclude_no_weights,
        test_random_with_exclude,
        test_random_with_exclude_all,
        test_random_with_weights,
        test_random_with_weights_and_exclude,
    ]


def test_cupertino_colors():
    for test in run_common_tests(ft.CupertinoColors):
        test()


def test_material_colors():
    for test in run_common_tests(ft.MaterialColors):
        test()

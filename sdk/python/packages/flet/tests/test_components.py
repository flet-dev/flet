def test_hash_args():
    import flet as ft

    @ft.component
    def MyComponent(x, y=0):
        return ft.Text(f"x: {x}, y: {y}")

    c = ft.Component(MyComponent)
    hash1 = c._hash_args((1,), {"y": 2})
    hash2 = c._hash_args((1,), {"y": 2})
    hash3 = c._hash_args((2,), {"y": 2})
    hash4 = c._hash_args((1,), {"y": 3})

    assert hash1 == hash2, "Hashes should be the same for identical args"
    assert hash1 != hash3, "Hashes should differ for different positional args"
    assert hash1 != hash4, "Hashes should differ for different keyword args"


def test_hash_args_with_observable():
    import flet as ft

    @ft.component
    def MyComponent(x, y=0):
        return ft.Text(f"x: {x}, y: {y}")

    obs = ft.Observable()
    obs.value = 10
    obs1 = ft.Observable()
    obs1.value = 20

    args = (1, "aaa", obs)
    kwargs = {"y": obs1}
    print("Args:", (args, kwargs))

    c = ft.Component(MyComponent)
    hash_1 = c._hash_args(args, kwargs)
    print(hash_1)

    obs.value = 15  # change observable
    print("Args:", (args, kwargs))

    hash_2 = c._hash_args(args, kwargs)
    print(hash_2)
    assert hash_1 != hash_2, "Hashes should differ when observable changes"

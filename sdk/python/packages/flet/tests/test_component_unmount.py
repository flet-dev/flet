from flet.components.component import Component


def test_will_unmount_releases_cached_render_references():
    """Unmounting drops the cached body, render arguments and contexts."""
    c = Component(fn=lambda: None, args=(1, 2, 3), kwargs={"k": "v"})
    c._state.mounted = True
    c._b = ["body"]
    c._state.last_b = ["memo-body"]
    c._state.last_args = ("a", "b")
    c._state.last_kwargs = {"x": "y"}
    c._contexts = {object(): object()}

    c.will_unmount()

    assert c._b is None
    assert c._state.last_b is None
    assert c._state.last_args == ()
    assert c._state.last_kwargs == {}
    assert c._contexts == {}

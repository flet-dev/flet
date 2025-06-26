import flet as ft


def test_controls_equality():
    t1 = ft.Text("A")
    t2 = ft.Text("A")
    assert t1 == t2

    t3 = ft.Text("B", data=1)
    t4 = ft.Text("B", data=2)
    assert t3 != t4

    c1 = ft.Column(
        [ft.Text("Some text"), ft.Button("Some button")], expand=True, data=1
    )
    c2 = ft.Column(
        [ft.Text("Some text"), ft.Button("Some button")], expand=True, data=1
    )
    assert c1 == c2


def test_keys():
    k1 = ft.ValueKey(1)
    assert str(k1) == "1"
    assert k1._type == "value"

    k2 = ft.ScrollKey("section_a")
    assert str(k2) == "section_a"
    assert k2._type == "scroll"

    t1 = ft.Text("A", key=ft.ValueKey("1"))
    t2 = ft.Text("A", key=ft.ValueKey("1"))
    assert t1 == t2

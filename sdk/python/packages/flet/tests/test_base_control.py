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

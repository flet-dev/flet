from flet import Textbox


def test_update_single_control(page):
    txt = Textbox(id="txt1", label="First name:")
    page.add(txt)
    page.update(txt)

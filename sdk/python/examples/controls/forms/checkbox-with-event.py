import flet
from flet import Checkbox, ElevatedButton, Text


def main(page):
  def checkbox_changed(e):
    t.value = f"Checkbox value changed to {c.value}" 
    t.update()

  c = Checkbox(label="Checkbox with 'change' event", on_change=checkbox_changed)
  t = Text()

  page.add(c, t)


flet.app(target=main)

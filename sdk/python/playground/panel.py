import flet
from flet import Button, Checkbox, Panel, Text

with flet.page("panel-custom") as page:

    def button_clicked(e):

        p.light_dismiss = light_dismiss.value
        p.auto_dismiss = auto_dismiss.value
        p.blocking = blocking.value
        values.value = (
            f"Panel properties are:  {p.light_dismiss}, {p.auto_dismiss}, {p.blocking}."
        )
        p.open = True
        page.update()

    values = Text()
    light_dismiss = Checkbox(label="Light dismiss", value=False)
    auto_dismiss = Checkbox(label="Auto-dismiss", value=True)
    blocking = Checkbox(label="Blocking", value=True)
    b = Button(text="Open panel", on_click=button_clicked)
    page.add(light_dismiss, auto_dismiss, blocking, b, values)

    t = Text("Content goes here")

    p = Panel(
        title="Panel with dismiss options",
        controls=[t],
    )

    page.add(p)

    input()

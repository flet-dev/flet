import flet

flet.run(
    lambda page: page.render(
        lambda: flet.Text("Hello, world!"),
    ),
)

import flet as ft

name = "SafeArea example"


def example():
    class State:
        counter = 0

    state = State()

    class Example(ft.SafeArea):
        def __init__(self):
            # super().__init__(ft.Container())
            super().__init__(content=ft.Container())
            self.counter = ft.Text("0", size=50)
            self.content = ft.Container(
                content=self.counter,
                alignment=ft.Alignment.CENTER,
            )
            self.expand = True

        # happens when example is added to the page
        def did_mount(self):
            self.page.floating_action_button = ft.FloatingActionButton(
                icon=ft.Icons.ADD,
                bgcolor=ft.Colors.LIME_300,
                data=0,
                on_click=fab_pressed,
            )
            self.page.update()

        # happens when example is removed from the page (when user chooses different control group on the menu)
        def will_unmount(self):
            self.page.floating_action_button = None
            print("Removing FAB")
            self.page.update()

    def fab_pressed(e):
        state.counter += 1
        example.counter.value = str(state.counter)
        example.counter.update()

    example = Example()
    return example

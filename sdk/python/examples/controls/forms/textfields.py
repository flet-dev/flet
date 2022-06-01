from time import sleep

import flet
from flet import Column, Page, ProgressBar, Text, TextField, icons, padding
from flet.progress_bar import ProgressBar
from flet.textfield import TextField


def main(page: Page):
    page.title = "TextField Examples"
    page.theme_mode = "light"
    page.padding = padding.all(20)

    page.splash = ProgressBar(visible=False)

    def chat_submit(e):
        print(f"Submit FieldText: {e.control.value}")
        e.control.value = ""
        form.disabled = True
        page.splash.visible = True
        page.update()
        sleep(2)
        form.disabled = False
        page.splash.visible = False
        page.update()

    chat_input = TextField(
        hint_text="Say something...",
        shift_enter=True,
        min_lines=1,
        on_submit=chat_submit,
        max_lines=5,
    )

    form = Column(
        [
            Text("Outlined TextField", style="headlineMedium"),
            TextField(),
            Text(
                "Outlined TextField with Label, Hint and Helper text",
                style="headlineSmall",
            ),
            TextField(
                label="Full name",
                hint_text="Enter your full name",
                helper_text="Hint text is visible when TextField is empty and focused",
            ),
            Text(
                "Underlined, filled and multiline TextField",
                style="headlineSmall",
            ),
            TextField(
                label="Comments",
                helper_text="Tell something about us",
                border="underline",
                filled=True,
                multiline=True,
            ),
            Text(
                "New line - Shift + Enter and submit on Enter",
                style="headlineSmall",
            ),
            chat_input,
            Text(
                "Login with email/password",
                style="headlineSmall",
            ),
            TextField(
                label="Email",
                prefix_icon=icons.EMAIL,
                border="underline",
                keyboard_type="email",
                filled=True,
            ),
            TextField(
                label="Password",
                prefix_icon=icons.PASSWORD_SHARP,
                border="underline",
                password=True,
                can_reveal_password=True,
                filled=True,
            ),
        ],
        scroll="adaptive",
        expand=1,
        width=600,
    )

    page.add(form)


flet.app(target=main)

# import logging

import flet
from flet import Button, Dialog, Stack, Text, Textbox
from flet.ref import Ref

# logging.basicConfig(level=logging.DEBUG)

pub_sub = {}


def broadcast(user, message):
    for session_id, handler in pub_sub.items():
        handler(user, message)


def main(page):

    page.padding = 10
    page.vertical_fill = True
    page.title = "Flet Chat Example"
    page.bgcolor = "neutralLight"
    page.theme = "light"  # "dark"

    username_dialog = Ref[Dialog]()
    username = Ref[Textbox]()
    messages = Ref[Stack]()
    message = Ref[Textbox]()

    def on_message(user, message):
        if user:
            messages.current.controls.append(Text(f"{user}: {message}"))
        else:
            messages.current.controls.append(
                Text(message, color="#888", size="small", italic=True)
            )
        page.update()

    pub_sub[page.session_id] = on_message

    def send_click(e):
        if message.current.value == "":
            return
        broadcast(page.user, message.current.value)
        message.current.value = ""
        page.update()

    page.user = page.session_id

    def join_click(e):
        if username.current.value == "":
            username.current.error_message = "Name cannot be blank!"
            username.current.update()
        else:
            page.user = username.current.value
            username_dialog.current.open = False
            # user_name.focused = False
            message.current.prefix = f"{page.user}:"
            message.current.focused = True
            page.update()
            broadcast(None, f"{page.user} entered the chat!")

    # layout
    page.add(
        Stack(
            height="100%",
            width="100%",
            bgcolor="white",
            padding=10,
            border_radius=5,
            vertical_align="end",
            controls=[Stack(ref=messages, scroll_y=True, auto_scroll=True)],
        ),
        Stack(
            horizontal=True,
            width="100%",
            controls=[
                Textbox(
                    ref=message,
                    width="100%",
                    multiline=True,
                    rows=1,
                    auto_adjust_height=True,
                    shift_enter=True,
                    resizable=False,
                ),
                Button("Send", primary=True, on_click=send_click),
            ],
            on_submit=send_click,
        ),
        Dialog(
            ref=username_dialog,
            open=True,
            blocking=True,
            auto_dismiss=False,
            title="Welcome!",
            controls=[Textbox(ref=username, label="Enter your name", focused=True)],
            footer=[Button(text="Join chat", primary=True, on_click=join_click)],
        ),
    )


flet.app("chat", target=main, share=False)

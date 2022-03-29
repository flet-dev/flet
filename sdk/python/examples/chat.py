import logging

import flet
from flet import Button, Dialog, Stack, Text, Textbox

logging.basicConfig(level=logging.DEBUG)

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

    messages = Stack(scroll_y=True, auto_scroll=True)
    messages_pane = Stack(
        height="100%",
        width="100%",
        bgcolor="white",
        padding=10,
        border_radius=5,
        vertical_align="end",
        controls=[messages],
    )
    message = Textbox(
        width="100%",
        multiline=True,
        rows=1,
        auto_adjust_height=True,
        shift_enter=True,
        resizable=False,
    )

    def on_message(user, message):
        if user:
            messages.controls.append(Text(f"{user}: {message}"))
        else:
            messages.controls.append(
                Text(message, color="#888", size="small", italic=True)
            )
        page.update()

    pub_sub[page.session_id] = on_message

    def send_click(e):
        if message.value == "":
            return
        broadcast(page.user, message.value)
        message.value = ""
        page.update()

    user_name = Textbox(label="Enter your name", focused=True)

    page.user = page.session_id

    def join_click(e):
        if user_name.value == "":
            user_name.error_message = "Name cannot be blank!"
            user_name.update()
        else:
            page.user = user_name.value
            dlg.open = False
            # user_name.focused = False
            message.prefix = f"{page.user}:"
            message.focused = True
            page.update()
            broadcast(None, f"{page.user} entered the chat!")

    dlg = Dialog(
        open=True,
        blocking=True,
        auto_dismiss=False,
        title="Welcome!",
        controls=[user_name],
        footer=[Button(text="Join chat", primary=True, on_click=join_click)],
    )

    send = Button("Send", primary=True, on_click=send_click)
    form = Stack(
        horizontal=True, width="100%", controls=[message, send], on_submit=send_click
    )
    page.add(messages_pane, form, dlg)


flet.app("chat", target=main, web=False)

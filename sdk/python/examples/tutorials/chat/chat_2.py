from dataclasses import dataclass

import flet as ft


@dataclass
class Message:
    user: str
    text: str


def main(page: ft.Page):
    chat = ft.Column()
    new_message = ft.TextField()

    def on_message(message: Message):
        chat.controls.append(ft.Text(f"{message.user}: {message.text}"))
        page.update()

    page.pubsub.subscribe(on_message)

    def send_click(e):
        page.pubsub.send_all(Message(user=page.session.id, text=new_message.value))
        new_message.value = ""

    page.add(chat, ft.Row([new_message, ft.Button("Send", on_click=send_click)]))


ft.run(main)

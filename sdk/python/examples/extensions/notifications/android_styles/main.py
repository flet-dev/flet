from datetime import datetime, timedelta
from pathlib import Path

import flet as ft
import flet_notifications as ftn

PICTURE = Path(__file__).parent / "assets" / "landscape.png"


async def main(page: ft.Page):
    if page.web or page.platform not in {
        ft.PagePlatform.ANDROID,
        ft.PagePlatform.ANDROID_TV,
    }:
        page.add(
            ft.SafeArea(
                content=ft.Text(
                    "Notification styles are an Android feature. "
                    "Run this example on Android."
                )
            )
        )
        return

    notifications = ftn.Notifications()

    async def show(id: int, title: str, body: str, style: ftn.AndroidStyle):
        await notifications.request_permissions()
        await notifications.show(
            id,
            title=title,
            body=body,
            options=ftn.NotificationOptions(android=ftn.AndroidOptions(style=style)),
        )

    async def big_text(e: ft.Event[ft.Button]):
        await show(
            1,
            "Release notes",
            "Version 2.0 is out",
            ftn.AndroidBigTextStyle(
                text="Version 2.0 brings offline mode, a redesigned editor, "
                "faster sync and dozens of fixes. Expand to read the highlights."
            ),
        )

    async def big_picture(e: ft.Event[ft.Button]):
        await show(
            2,
            "Photo shared",
            "Ada shared a photo",
            ftn.AndroidBigPictureStyle(
                image=ftn.AndroidBytesBitmap(data=PICTURE.read_bytes()),
                summary_text="Hills at sunrise",
            ),
        )

    async def inbox(e: ft.Event[ft.Button]):
        await show(
            3,
            "3 new emails",
            "From Ada, Grace and Alan",
            ftn.AndroidInboxStyle(
                lines=["Ada: Lunch tomorrow?", "Grace: Slides attached", "Alan: Ping"],
                summary_text="work@example.com",
            ),
        )

    async def messaging(e: ft.Event[ft.Button]):
        me = ftn.AndroidPerson(name="You")
        ada = ftn.AndroidPerson(name="Ada")
        now = datetime.now().astimezone()
        await show(
            4,
            "Ada",
            "See you there",
            ftn.AndroidMessagingStyle(
                person=me,
                conversation_title="Lunch",
                messages=[
                    ftn.AndroidMessage(
                        text="Noon at the usual place?",
                        timestamp=now - timedelta(minutes=2),
                        person=ada,
                    ),
                    ftn.AndroidMessage(text="Sure!", timestamp=now, person=me),
                ],
            ),
        )

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Button("Big text", on_click=big_text),
                    ft.Button("Big picture", on_click=big_picture),
                    ft.Button("Inbox", on_click=inbox),
                    ft.Button("Messaging", on_click=messaging),
                ]
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)

import flet as ft


async def main(page: ft.Page):
    share = ft.Share()

    status = ft.Text()
    result_raw = ft.Text()

    async def do_share_text():
        result = await share.share_text(
            "Hello from Flet!",
            subject="Greeting",
            title="Share greeting",
        )
        status.value = f"Share status: {result.status}"
        result_raw.value = f"Raw: {result.raw}"

    async def do_share_uri():
        result = await share.share_uri("https://flet.dev")
        status.value = f"Share status: {result.status}"
        result_raw.value = f"Raw: {result.raw}"

    async def do_share_files():
        file = ft.ShareFile.from_bytes(
            b"Sample content from memory",
            mime_type="text/plain",
            name="sample.txt",
        )
        result = await share.share_files(
            [file],
            text="Sharing a file from memory",
        )
        status.value = f"Share status: {result.status}"
        result_raw.value = f"Raw: {result.raw}"

    page.add(
        ft.SafeArea(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Button("Share text", on_click=do_share_text),
                            ft.Button("Share link", on_click=do_share_uri),
                            ft.Button("Share file", on_click=do_share_files),
                        ],
                        wrap=True,
                    ),
                    status,
                    result_raw,
                ],
            )
        )
    )


ft.run(main)

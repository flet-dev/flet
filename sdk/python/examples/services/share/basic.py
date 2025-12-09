import os

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

    async def do_share_files_from_bytes():
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

    async def do_share_files_from_paths():
        if page.web:
            status.value = "File sharing from paths is not supported on the web."
            return
        #
        temp_dir = await ft.StoragePaths().get_temporary_directory()
        file_path = os.path.join(temp_dir, "sample_from_path.txt")
        with open(file_path, "wb") as f:
            f.write(b"Sample content from file path")

        result = await share.share_files(
            [ft.ShareFile.from_path(file_path)],
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
                            ft.Button(
                                "Share file from bytes",
                                on_click=do_share_files_from_bytes,
                            ),
                            ft.Button(
                                "Share file from path",
                                on_click=do_share_files_from_paths,
                            ),
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

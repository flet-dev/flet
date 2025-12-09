import flet as ft


async def main(page: ft.Page):
    url_launcher = ft.UrlLauncher()

    url = ft.TextField(label="URL to open", value="https://flet.dev", expand=True)
    status = ft.Text()

    async def can_launch():
        can = await url_launcher.can_launch_url(url.value)
        status.value = f"Can launch: {can}"

    async def launch_default():
        await url_launcher.launch_url(url.value)

    async def launch_in_app_webview():
        await url_launcher.launch_url(
            url.value,
            mode=ft.LaunchMode.IN_APP_WEB_VIEW,
            web_view_configuration=ft.WebViewConfiguration(
                enable_javascript=True, enable_dom_storage=True
            ),
        )

    async def launch_in_app_browser_view():
        await url_launcher.launch_url(
            url.value,
            mode=ft.LaunchMode.IN_APP_BROWSER_VIEW,
            browser_configuration=ft.BrowserConfiguration(show_title=True),
        )

    async def launch_external():
        await url_launcher.launch_url(
            url.value,
            mode=ft.LaunchMode.EXTERNAL_APPLICATION,
            web_only_window_name="_blank",
        )

    async def launch_popup():
        await url_launcher.open_window(
            url.value, title="Flet popup", width=480, height=640
        )

    async def close_webview(_):
        supported = await url_launcher.supports_close_for_launch_mode(
            ft.LaunchMode.IN_APP_WEB_VIEW
        )
        if supported:
            await url_launcher.close_in_app_web_view()
        else:
            status.value = "Close in-app web view not supported on this platform"

    page.add(
        ft.Column(
            [
                url,
                ft.Row(
                    [
                        ft.Button("Launch URL", on_click=launch_default),
                        ft.Button(
                            "Launch in-app webview", on_click=launch_in_app_webview
                        ),
                        ft.Button(
                            "Launch in-app browser view",
                            on_click=launch_in_app_browser_view,
                        ),
                        ft.Button("Launch external/new tab", on_click=launch_external),
                        ft.Button("Open popup window (web)", on_click=launch_popup),
                        ft.Button("Can launch?", on_click=can_launch),
                        ft.Button("Close in-app webview", on_click=close_webview),
                    ],
                    wrap=True,
                ),
                status,
            ],
        )
    )


ft.run(main)

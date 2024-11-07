from flet.utils.platform_utils import is_mobile


def open_in_browser(url):
    if not is_mobile():
        import webbrowser

        webbrowser.open(url)


from flet.utils.platform_utils import is_mobile


def open_in_browser(url: str):
    """
    Opens a URL in the system default browser on non-mobile platforms.

    On mobile targets, this function does nothing.

    Args:
        url: URL to open.
    """
    if not is_mobile():
        import webbrowser

        webbrowser.open(url)

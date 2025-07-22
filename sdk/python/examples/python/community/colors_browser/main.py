import time

import flet
from flet import (
    AppBar,
    ButtonStyle,
    ControlEvent,
    IconButton,
    Page,
    ProgressBar,
    Row,
    Text,
    TextButton,
    colors,
    icons,
)

# importing version 1
from v1 import ColorBrowser1

# importing version 2
from v2 import ColorBrowser2


def main(page: Page):
    """
    App's entry point.

    :param page: The page object
    :type page: Page
    """
    page.title = "Flet Colors Browser"
    # page.window_always_on_top = True

    # set the minimum width and height of the window.
    page.window_min_width = 245
    page.window_min_height = 406

    # Setting the theme of the page to light mode.
    page.theme_mode = "light"

    # set the width and height of the window.
    page.window_width = 562
    page.window_height = 720

    # Creating a progress bar that will be used to show the user that the app is busy doing something.
    page.splash = ProgressBar(visible=False)

    def change_theme(e):
        """
        When the button(to change theme) is clicked, the progress bar is made visible, the theme is changed,
        the progress bar is made invisible, and the page is updated

        :param e: The event that triggered the function
        """
        page.splash.visible = True
        page.update()
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        page.splash.visible = False
        theme_icon_button.selected = not theme_icon_button.selected
        time.sleep(1.2)
        page.update()

    def moveto_callback(e: ControlEvent):
        # Making the progress bar visible and updating the page.
        page.splash.visible = True
        page.update()

        # Changing the version of the page. (Removes the currently shown version, and adds the next version to the page
        last_version = page.controls.pop(0)
        if last_version == version_1:
            page.controls.insert(0, version_2)
        else:
            page.controls.insert(0, version_1)

        # Changing the text of the button to "Move to Version 2" if the text is "Move to Version 1", and vice versa.
        e.control.text = (
            "Move to Version 2"
            if e.control.text == "Move to Version 1"
            else "Move to Version 1"
        )

        # Making the progress bar invisible, waiting for 1.2 seconds, then updating the page.
        page.splash.visible = False
        time.sleep(1.2)
        page.update()

    # button to change theme_mode (from dark to light mode, or the reverse)
    theme_icon_button = IconButton(
        icons.DARK_MODE,
        selected_icon=icons.LIGHT_MODE,
        icon_color=colors.BLACK,
        icon_size=35,
        tooltip="change theme",
        on_click=change_theme,
        style=ButtonStyle(
            color={"": colors.BLACK, "selected": colors.WHITE},
        ),
    )

    moveto_button = TextButton(
        "Move to Version 1",
        on_click=moveto_callback,
        tooltip="change version",
        icon=icons.KEYBOARD_BACKSPACE_ROUNDED,
        icon_color=colors.ERROR,
    )

    page.appbar = AppBar(
        title=Text("Colors Browser", color="white"),
        center_title=True,
        bgcolor="blue",
        actions=[theme_icon_button],
    )

    # Creating two versions of the page, one with the colors in a grid, and the other with the colors in a list.
    version_1 = ColorBrowser1()
    version_2 = ColorBrowser2(page)

    page.add(
        version_2,
        Row(
            [moveto_button],
            alignment="start",
        ),
    )


# (running the app)
if __name__ == "__main__":
    flet.app(target=main)
# OR flet.app(target=main, view=flet.WEB_BROWSER, port=5050) then open http://localhost:5050/

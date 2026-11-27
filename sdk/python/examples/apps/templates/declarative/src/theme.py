"""Design tokens. Views use these names, never raw colours, sizes or paddings."""

import flet as ft

SEED = "#3F6FD8"  # pick a colour for the app's subject


class Space:
    XS = 4
    S = 8
    M = 12
    L = 16
    XL = 24
    XXL = 32


class Radius:
    S = 8
    M = 12
    L = 16


class Text:
    DISPLAY = ft.TextThemeStyle.DISPLAY_SMALL  # big numbers
    TITLE = ft.TextThemeStyle.TITLE_MEDIUM  # section and row titles
    BODY = ft.TextThemeStyle.BODY_MEDIUM
    LABEL = ft.TextThemeStyle.LABEL_MEDIUM  # captions, secondary info


MAX_CONTENT_WIDTH = 720  # content column on wide screens
COMPACT_BREAKPOINT = 600  # below: bottom NavigationBar + FAB; above: NavigationRail


def build_theme() -> ft.Theme:
    return ft.Theme(color_scheme_seed=SEED)


def build_dark_theme() -> ft.Theme:
    return ft.Theme(color_scheme_seed=SEED)

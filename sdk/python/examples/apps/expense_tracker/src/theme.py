"""Design tokens. Views use these names, never raw colours, sizes or paddings."""

import flet as ft

SEED = "#237457"  # deep ledger green
LINE_WIDTH = 1
LIST_BOTTOM_SPACE = 96
CHART_HEIGHT = 240
PIE_RADIUS = 100
CHART_AXIS_WIDTH = 48
CHART_LABEL_HEIGHT = 32
CHART_BAR_WIDTH = 22
LEGEND_DOT_SIZE = 12
CATEGORY_COLORS = {
    "teal": ft.Colors.TEAL_400,
    "indigo": ft.Colors.INDIGO_300,
    "amber": ft.Colors.AMBER_600,
    "pink": ft.Colors.PINK_300,
    "slate": ft.Colors.BLUE_GREY_400,
    "blue": ft.Colors.BLUE_400,
    "purple": ft.Colors.PURPLE_300,
    "orange": ft.Colors.ORANGE_600,
}
CATEGORY_ICON_SIZE = 32
BUDGET_BAR_HEIGHT = 8
RECEIPT_PREVIEW_HEIGHT = 200
RECEIPT_DETAIL_HEIGHT = 360
CAMERA_PREVIEW_HEIGHT = 360


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

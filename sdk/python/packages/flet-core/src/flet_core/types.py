from enum import Enum
from typing import Dict, Tuple, Union

from flet_core.animation import Animation
from flet_core.border_radius import BorderRadius
from flet_core.margin import Margin
from flet_core.padding import Padding
from flet_core.transform import Offset, Rotate, Scale

WEB_BROWSER = "web_browser"
FLET_APP = "flet_app"
FLET_APP_WEB = "flet_app_web"
FLET_APP_HIDDEN = "flet_app_hidden"


class AppView(Enum):
    WEB_BROWSER = "web_browser"
    FLET_APP = "flet_app"
    FLET_APP_WEB = "flet_app_web"
    FLET_APP_HIDDEN = "flet_app_hidden"


class WebRenderer(Enum):
    AUTO = "auto"
    HTML = "html"
    CANVAS_KIT = "canvaskit"


class UrlTarget(Enum):
    BLANK = "blank"
    SELF = "_self"
    PARENT = "_parent"
    TOP = "_top"
    # UNFENCED_TOP = "_unfencedTop"


PaddingValue = Union[None, int, float, Padding]

MarginValue = Union[None, int, float, Margin]

BorderRadiusValue = Union[None, int, float, BorderRadius]

RotateValue = Union[None, int, float, Rotate]

ScaleValue = Union[None, int, float, Scale]

OffsetValue = Union[None, Offset, Tuple[Union[float, int], Union[float, int]]]

AnimationValue = Union[None, bool, int, Animation]


class FontWeight(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    W_100 = "w100"
    W_200 = "w200"
    W_300 = "w300"
    W_400 = "w400"
    W_500 = "w500"
    W_600 = "w600"
    W_700 = "w700"
    W_800 = "w800"
    W_900 = "w900"


class BoxShape(Enum):
    RECTANGLE = "rectangle"
    CIRCLE = "circle"


class NotchShape(Enum):
    AUTO = "auto"
    CIRCULAR = "circular"


ResponsiveNumber = Union[Dict[str, Union[int, float]], int, float]


class MaterialState(Enum):
    HOVERED = "hovered"
    FOCUSED = "focused"
    PRESSED = "pressed"
    DRAGGED = "dragged"
    SELECTED = "selected"
    SCROLLED_UNDER = "scrolledUnder"
    DISABLED = "disabled"
    ERROR = "error"
    DEFAULT = ""


class MainAxisAlignment(Enum):
    START = "start"
    END = "end"
    CENTER = "center"
    SPACE_BETWEEN = "spaceBetween"
    SPACE_AROUND = "spaceAround"
    SPACE_EVENLY = "spaceEvenly"


class CrossAxisAlignment(Enum):
    START = "start"
    END = "end"
    CENTER = "center"
    STRETCH = "stretch"
    BASELINE = "baseline"


class VerticalAlignment(Enum):
    NONE = None
    START = -1.0
    END = 1.0
    CENTER = 0.0


class TabAlignment(Enum):
    START = "start"
    START_OFFSET = "startOffset"
    FILL = "fill"
    CENTER = "center"


class LabelPosition(Enum):
    RIGHT = "right"
    LEFT = "left"


class BlendMode(Enum):
    CLEAR = "clear"
    COLOR = "color"
    COLOR_BURN = "colorBurn"
    COLOR_DODGE = "colorDodge"
    DARKEN = "darken"
    DIFFERENCE = "difference"
    DST = "dst"
    DST_A_TOP = "dstATop"
    DST_IN = "dstIn"
    DST_OUT = "dstOut"
    DST_OVER = "dstOver"
    EXCLUSION = "exclusion"
    HARD_LIGHT = "hardLight"
    HUE = "hue"
    LIGHTEN = "lighten"
    LUMINOSITY = "luminosity"
    MODULATE = "modulate"
    MULTIPLY = "multiply"
    OVERLAY = "overlay"
    PLUS = "plus"
    SATURATION = "saturation"
    SCREEN = "screen"
    SOFT_LIGHT = "softLight"
    SRC = "src"
    SRC_A_TOP = "srcATop"
    SRC_IN = "srcIn"
    SRC_OUT = "srcOut"
    SRC_OVER = "srcOver"
    VALUES = "values"
    XOR = "xor"


class TextAlign(Enum):
    LEFT = "left"
    RIGHT = "right"
    CENTER = "center"
    JUSTIFY = "justify"
    START = "start"
    END = "end"


class ScrollMode(Enum):
    AUTO = "auto"
    ADAPTIVE = "adaptive"
    ALWAYS = "always"
    HIDDEN = "hidden"


class ClipBehavior(Enum):
    NONE = "none"
    ANTI_ALIAS = "antiAlias"
    ANTI_ALIAS_WITH_SAVE_LAYER = "antiAliasWithSaveLayer"
    HARD_EDGE = "hardEdge"


class ImageFit(Enum):
    NONE = "none"
    CONTAIN = "contain"
    COVER = "cover"
    FILL = "fill"
    FIT_HEIGHT = "fitHeight"
    FIT_WIDTH = "fitWidth"
    SCALE_DOWN = "scaleDown"


class ImageRepeat(Enum):
    NO_REPEAT = "noRepeat"
    REPEAT = "repeat"
    REPEAT_X = "repeatX"
    REPEAT_Y = "repeatY"


class PagePlatform(Enum):
    IOS = "ios"
    ANDROID = "android"
    MACOS = "macos"
    WINDOWS = "windows"
    LINUX = "linux"


class ThemeMode(Enum):
    SYSTEM = "system"
    LIGHT = "light"
    DARK = "dark"


class Brightness(Enum):
    LIGHT = "light"
    DARK = "dark"


class Orientation(Enum):
    PORTRAIT = "portrait"
    LANDSCAPE = "landscape"


class FloatingActionButtonLocation(Enum):
    CENTER_DOCKED = "centerDocked"
    CENTER_FLOAT = "centerFloat"
    CENTER_TOP = "centerTop"
    END_CONTAINED = "endContained"
    END_DOCKED = "endDocked"
    END_FLOAT = "endFloat"
    END_TOP = "endTop"
    MINI_CENTER_DOCKED = "miniCenterDocked"
    MINI_CENTER_FLOAT = "miniCenterFloat"
    MINI_CENTER_TOP = "miniCenterTop"
    MINI_END_DOCKED = "miniEndDocked"
    MINI_END_FLOAT = "miniEndFloat"
    MINI_END_TOP = "miniEndTop"
    MINI_START_DOCKED = "miniStartDocked"
    MINI_START_FLOAT = "miniStartFloat"
    MINI_START_TOP = "miniStartTop"
    START_DOCKED = "startDocked"
    START_FLOAT = "startFloat"
    START_TOP = "startTop"


class AppLifecycleState(Enum):
    SHOW = "show"
    RESUME = "resume"
    HIDE = "hide"
    INACTIVE = "inactive"
    PAUSE = "pause"
    DETACH = "detach"
    RESTART = "restart"


class MouseCursor(Enum):
    ALIAS = "alias"
    ALL_SCROLL = "allScroll"
    BASIC = "basic"
    CELL = "cell"
    CLICK = "click"
    CONTEXT_MENU = "contextMenu"
    COPY = "copy"
    DISAPPEARING = "disappearing"
    FORBIDDEN = "forbidden"
    GRAB = "grab"
    GRABBING = "grabbing"
    HELP = "help"
    MOVE = "move"
    NO_DROP = "noDrop"
    NONE = "none"
    PRECISE = "precise"
    PROGRESS = "progress"
    RESIZE_COLUMN = "resizeColumn"
    RESIZE_DOWN = "resizeDown"
    RESIZE_DOWN_LEFT = "resizeDownLeft"
    RESIZE_DOWN_RIGHT = "resizeDownRight"
    RESIZE_LEFT = "resizeLeft"
    RESIZE_LEFT_RIGHT = "resizeLeftRight"
    RESIZE_RIGHT = "resizeRight"
    RESIZE_ROW = "resizeRow"
    RESIZE_UP = "resizeUp"
    RESIZE_UP_DOWN = "resizeUpDown"
    RESIZE_UP_LEFT = "resizeUpLeft"
    RESIZE_UP_LEFT_DOWN_RIGHT = "resizeUpLeftDownRight"
    RESIZE_UP_RIGHT = "resizeUpRight"
    RESIZE_UP_RIGHT_DOWN_LEFT = "resizeUpRightDownLeft"
    TEXT = "text"
    VERTICAL_TEXT = "verticalText"
    WAIT = "wait"
    ZOOM_IN = "zoomIn"
    ZOOM_OUT = "zoomOut"


class AutoFillHint(Enum):
    ADDRESS_CITY = "addressCity"
    ADDRESS_CITY_AND_STATE = "addressCityAndState"
    ADDRESS_STATE = "addressState"
    BIRTHDAY = "birthday"
    BIRTHDAY_DAY = "birthdayDay"
    BIRTHDAY_MONTH = "birthdayMonth"
    BIRTHDAY_YEAR = "birthdayYear"
    COUNTRY_CODE = "countryCode"
    COUNTRY_NAME = "countryName"
    CREDIT_CARD_EXPIRATION_DATE = "creditCardExpirationDate"
    CREDIT_CARD_EXPIRATION_DAY = "creditCardExpirationDay"
    CREDIT_CARD_EXPIRATION_MONTH = "creditCardExpirationMonth"
    CREDIT_CARD_EXPIRATION_YEAR = "creditCardExpirationYear"
    CREDIT_CARD_FAMILY_NAME = "creditCardFamilyName"
    CREDIT_CARD_GIVEN_NAME = "creditCardGivenName"
    CREDIT_CARD_MIDDLE_NAME = "creditCardMiddleName"
    CREDIT_CARD_NAME = "creditCardName"
    CREDIT_CARD_NUMBER = "creditCardNumber"
    CREDIT_CARD_SECURITY_CODE = "creditCardSecurityCode"
    CREDIT_CARD_TYPE = "creditCardType"
    EMAIL = "email"
    FAMILY_NAME = "familyName"
    FULL_STREET_ADDRESS = "fullStreetAddress"
    GENDER = "gender"
    GIVEN_NAME = "givenName"
    IMPP = "impp"
    JOB_TITLE = "jobTitle"
    LANGUAGE = "language"
    LOCATION = "location"
    MIDDLE_INITIAL = "middleInitial"
    MIDDLE_NAME = "middleName"
    NAME = "name"
    NAME_PREFIX = "namePrefix"
    NAME_SUFFIX = "nameSuffix"
    NEW_PASSWORD = "newPassword"
    NEW_USERNAME = "newUsername"
    NICKNAME = "nickname"
    ONE_TIME_CODE = "oneTimeCode"
    ORGANIZATION_NAME = "organizationName"
    PASSWORD = "password"
    PHOTO = "photo"
    POSTAL_ADDRESS = "postalAddress"
    POSTAL_ADDRESS_EXTENDED = "postalAddressExtended"
    POSTAL_ADDRESS_EXTENDED_POSTAL_CODE = "postalAddressExtendedPostalCode"
    POSTAL_CODE = "postalCode"
    STREET_ADDRESS_LEVEL1 = "streetAddressLevel1"
    STREET_ADDRESS_LEVEL2 = "streetAddressLevel2"
    STREET_ADDRESS_LEVEL3 = "streetAddressLevel3"
    STREET_ADDRESS_LEVEL4 = "streetAddressLevel4"
    STREET_ADDRESS_LINE1 = "streetAddressLine1"
    STREET_ADDRESS_LINE2 = "streetAddressLine2"
    STREET_ADDRESS_LINE3 = "streetAddressLine3"
    SUB_LOCALITY = "sublocality"
    TELEPHONE_NUMBER = "telephoneNumber"
    TELEPHONE_NUMBER_AREA_CODE = "telephoneNumberAreaCode"
    TELEPHONE_NUMBER_COUNTRY_CODE = "telephoneNumberCountryCode"
    TELEPHONE_NUMBER_DEVICE = "telephoneNumberDevice"
    TELEPHONE_NUMBER_EXTENSION = "telephoneNumberExtension"
    TELEPHONE_NUMBER_LOCAL = "telephoneNumberLocal"
    TELEPHONE_NUMBER_LOCAL_PREFIX = "telephoneNumberLocalPrefix"
    TELEPHONE_NUMBER_LOCAL_SUFFIX = "telephoneNumberLocalSuffix"
    TELEPHONE_NUMBER_NATIONAL = "telephoneNumberNational"
    TRANSACTION_AMOUNT = "transactionAmount"
    TRANSACTION_CURRENCY = "transactionCurrency"
    URL = "url"
    USERNAME = "username"

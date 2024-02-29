"""
url='https://raw.githubusercontent.com/flutter/flutter/stable/packages/flutter/lib/src/cupertino/colors.dart'
output_file="$HOME/cupertino_python_colors.txt"
curl -s $url | python -c '
import re

for line in __import__("sys").stdin:
    match1 = re.search(r"static const CupertinoDynamicColor ([a-zA-Z0-9_]+)", line)
    match2 = re.search(r"static const Color ([a-zA-Z0-9_]+)", line)
    if match1:
        print("{} = \"{}\"".format(match1.group(1).upper(), match1.group(1)))
    elif match2:
        print("{} = \"{}\"".format(match2.group(1).upper(), match2.group(1)))
' >> "$output_file"
"""

PRIMARY = "primary"
ON_PRIMARY = "onprimary"
ACTIVE_BLUE = "activeBlue"
ACTIVE_GREEN = "activeGreen"
ACTIVE_ORANGE = "activeOrange"
WHITE = "cupertinoWhite"
BLACK = "cupertinoBlack"
LIGHT_BACKGROUND_GRAY = "lightBackgroundGray"
EXTRA_LIGHT_BACKGROUND_GRAY = "extraLightBackgroundGray"
DARK_BACKGROUND_GRAY = "darkBackgroundGray"
INACTIVE_GRAY = "inactiveGray"
DESTRUCTIVE_RED = "destructiveRed"
SYSTEM_BLUE = "systemBlue"
SYSTEM_GREEN = "systemGreen"
SYSTEM_MINT = "systemMint"
SYSTEM_INDIGO = "systemIndigo"
SYSTEM_ORANGE = "systemOrange"
SYSTEM_PINK = "systemPink"
SYSTEM_BROWN = "systemBrown"
SYSTEM_PURPLE = "systemPurple"
SYSTEM_RED = "systemRed"
SYSTEM_TEAL = "systemTeal"
SYSTEM_CYAN = "systemCyan"
SYSTEM_YELLOW = "systemYellow"
SYSTEM_GREY = "systemGrey"
SYSTEM_GREY2 = "systemGrey2"
SYSTEM_GREY3 = "systemGrey3"
SYSTEM_GREY4 = "systemGrey4"
SYSTEM_GREY5 = "systemGrey5"
SYSTEM_GREY6 = "systemGrey6"
LABEL = "label"
SECONDARY_LABEL = "secondaryLabel"
TERTIARY_LABEL = "tertiaryLabel"
QUATERNARY_LABEL = "quaternaryLabel"
SYSTEM_FILL = "systemFill"
SECONDARY_SYSTEM_FILL = "secondarySystemFill"
TERTIARY_SYSTEM_FILL = "tertiarySystemFill"
QUATERNARY_SYSTEM_FILL = "quaternarySystemFill"
PLACEHOLDER_TEXT = "placeholderText"
SYSTEM_BACKGROUND = "systemBackground"
SECONDARY_SYSTEM_BACKGROUND = "secondarySystemBackground"
TERTIARY_SYSTEM_BACKGROUND = "tertiarySystemBackground"
SYSTEM_GROUPED_BACKGROUND = "systemGroupedBackground"
SECONDARY_SYSTEM_GROUPED_BACKGROUND = "secondarySystemGroupedBackground"
TERTIARY_SYSTEM_GROUPED_BACKGROUND = "tertiarySystemGroupedBackground"
SEPARATOR = "separator"
OPAQUE_SEPARATOR = "opaqueSeparator"
LINK = "link"

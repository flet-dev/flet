import 'package:flutter/cupertino.dart';

// Bash script to generate colors list
//
/*

url='https://raw.githubusercontent.com/flutter/flutter/master/packages/flutter/lib/src/cupertino/colors.dart'
output_file="$HOME/cupertino_colors.txt"

echo "Map<String, Color> cupertinoColors = {" > "$output_file"

curl -s $url | python -c '
import re

for line in __import__("sys").stdin:
    match1 = re.search(r"static const CupertinoDynamicColor ([a-zA-Z0-9_]+)", line)
    match2 = re.search(r"static const Color ([a-zA-Z0-9_]+)", line)
    if match1:
        print("\"{}\": CupertinoColors.{}, ".format(match1.group(1), match1.group(1)))
    elif match2:
        print("\"{}\": CupertinoColors.{}, ".format(match2.group(1), match2.group(1)))

' >> "$output_file"

echo "};" >> "$output_file"

*/

Map<String, Color> cupertinoColors = {
"activeBlue": CupertinoColors.activeBlue,
"activeGreen": CupertinoColors.activeGreen,
"activeOrange": CupertinoColors.activeOrange,
"white": CupertinoColors.white,
"black": CupertinoColors.black,
"lightBackgroundGray": CupertinoColors.lightBackgroundGray,
"extraLightBackgroundGray": CupertinoColors.extraLightBackgroundGray,
"darkBackgroundGray": CupertinoColors.darkBackgroundGray,
"inactiveGray": CupertinoColors.inactiveGray,
"destructiveRed": CupertinoColors.destructiveRed,
"systemBlue": CupertinoColors.systemBlue,
"systemGreen": CupertinoColors.systemGreen,
"systemMint": CupertinoColors.systemMint,
"systemIndigo": CupertinoColors.systemIndigo,
"systemOrange": CupertinoColors.systemOrange,
"systemPink": CupertinoColors.systemPink,
"systemBrown": CupertinoColors.systemBrown,
"systemPurple": CupertinoColors.systemPurple,
"systemRed": CupertinoColors.systemRed,
"systemTeal": CupertinoColors.systemTeal,
"systemCyan": CupertinoColors.systemCyan,
"systemYellow": CupertinoColors.systemYellow,
"systemGrey": CupertinoColors.systemGrey,
"systemGrey2": CupertinoColors.systemGrey2,
"systemGrey3": CupertinoColors.systemGrey3,
"systemGrey4": CupertinoColors.systemGrey4,
"systemGrey5": CupertinoColors.systemGrey5,
"systemGrey6": CupertinoColors.systemGrey6,
"label": CupertinoColors.label,
"secondaryLabel": CupertinoColors.secondaryLabel,
"tertiaryLabel": CupertinoColors.tertiaryLabel,
"quaternaryLabel": CupertinoColors.quaternaryLabel,
"systemFill": CupertinoColors.systemFill,
"secondarySystemFill": CupertinoColors.secondarySystemFill,
"tertiarySystemFill": CupertinoColors.tertiarySystemFill,
"quaternarySystemFill": CupertinoColors.quaternarySystemFill,
"placeholderText": CupertinoColors.placeholderText,
"systemBackground": CupertinoColors.systemBackground,
"secondarySystemBackground": CupertinoColors.secondarySystemBackground,
"tertiarySystemBackground": CupertinoColors.tertiarySystemBackground,
"systemGroupedBackground": CupertinoColors.systemGroupedBackground,
"secondarySystemGroupedBackground": CupertinoColors.secondarySystemGroupedBackground,
"tertiarySystemGroupedBackground": CupertinoColors.tertiarySystemGroupedBackground,
"separator": CupertinoColors.separator,
"opaqueSeparator": CupertinoColors.opaqueSeparator,
"link": CupertinoColors.link,
};

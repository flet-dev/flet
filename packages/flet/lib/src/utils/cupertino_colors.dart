import 'package:flutter/cupertino.dart';

// Bash script to generate colors list
//
/*

url='https://raw.githubusercontent.com/flutter/flutter/stable/packages/flutter/lib/src/cupertino/colors.dart'
output_file="$HOME/cupertino_colors.txt"

echo "Map<String, Color> cupertinoColors = {" > "$output_file"

curl -s $url | python -c '
import re

for line in __import__("sys").stdin:
    match1 = re.search(r"static const CupertinoDynamicColor ([a-zA-Z0-9_]+)", line)
    match2 = re.search(r"static const Color ([a-zA-Z0-9_]+)", line)
    if match1:
        print("\"{}\": CupertinoColors.{}, ".format(match1.group(1).lower(), match1.group(1)))
    elif match2:
        print("\"{}\": CupertinoColors.{}, ".format(match2.group(1).lower(), match2.group(1)))

' >> "$output_file"

echo "};" >> "$output_file"

*/

Map<String, Color> cupertinoColors = {
  "activeblue": CupertinoColors.activeBlue,
  "activegreen": CupertinoColors.activeGreen,
  "activeorange": CupertinoColors.activeOrange,
  "cupertinowhite": CupertinoColors.white,
  "cupertinoblack": CupertinoColors.black,
  "lightbackgroundgray": CupertinoColors.lightBackgroundGray,
  "extralightbackgroundgray": CupertinoColors.extraLightBackgroundGray,
  "darkbackgroundgray": CupertinoColors.darkBackgroundGray,
  "inactivegray": CupertinoColors.inactiveGray,
  "destructivered": CupertinoColors.destructiveRed,
  "systemblue": CupertinoColors.systemBlue,
  "systemgreen": CupertinoColors.systemGreen,
  "systemmint": CupertinoColors.systemMint,
  "systemindigo": CupertinoColors.systemIndigo,
  "systemorange": CupertinoColors.systemOrange,
  "systempink": CupertinoColors.systemPink,
  "systembrown": CupertinoColors.systemBrown,
  "systempurple": CupertinoColors.systemPurple,
  "systemred": CupertinoColors.systemRed,
  "systemteal": CupertinoColors.systemTeal,
  "systemcyan": CupertinoColors.systemCyan,
  "systemyellow": CupertinoColors.systemYellow,
  "systemgrey": CupertinoColors.systemGrey,
  "systemgrey2": CupertinoColors.systemGrey2,
  "systemgrey3": CupertinoColors.systemGrey3,
  "systemgrey4": CupertinoColors.systemGrey4,
  "systemgrey5": CupertinoColors.systemGrey5,
  "systemgrey6": CupertinoColors.systemGrey6,
  "label": CupertinoColors.label,
  "secondarylabel": CupertinoColors.secondaryLabel,
  "tertiarylabel": CupertinoColors.tertiaryLabel,
  "quaternarylabel": CupertinoColors.quaternaryLabel,
  "systemfill": CupertinoColors.systemFill,
  "secondarysystemfill": CupertinoColors.secondarySystemFill,
  "tertiarysystemfill": CupertinoColors.tertiarySystemFill,
  "quaternarysystemfill": CupertinoColors.quaternarySystemFill,
  "placeholdertext": CupertinoColors.placeholderText,
  "systembackground": CupertinoColors.systemBackground,
  "secondarysystembackground": CupertinoColors.secondarySystemBackground,
  "tertiarysystembackground": CupertinoColors.tertiarySystemBackground,
  "systemgroupedbackground": CupertinoColors.systemGroupedBackground,
  "secondarysystemgroupedbackground":
      CupertinoColors.secondarySystemGroupedBackground,
  "tertiarysystemgroupedbackground":
      CupertinoColors.tertiarySystemGroupedBackground,
  "separator": CupertinoColors.separator,
  "opaqueseparator": CupertinoColors.opaqueSeparator,
  "link": CupertinoColors.link,
};

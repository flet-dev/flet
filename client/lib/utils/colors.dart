import 'dart:ui';

import 'package:flutter/material.dart';

Map<String, MaterialColor> _materialColors = {
  "red": Colors.red,
  "pink": Colors.pink,
  "purple": Colors.purple,
  "deeppurple": Colors.deepPurple,
  "indigo": Colors.indigo,
  "blue": Colors.blue,
  "lightblue": Colors.lightBlue,
  "cyan": Colors.cyan,
  "teal": Colors.teal,
  "green": Colors.green,
  "lightgreen": Colors.lightGreen,
  "lime": Colors.lime,
  "yellow": Colors.yellow,
  "amber": Colors.amber,
  "orange": Colors.orange,
  "deeporange": Colors.deepOrange,
  "brown": Colors.brown,
  "bluegrey": Colors.blueGrey,
};

Map<String, MaterialAccentColor> _materialAccentColors = {
  "redaccent": Colors.redAccent,
  "pinkaccent": Colors.pinkAccent,
  "purpleaccent": Colors.purpleAccent,
  "deeppurpleaccent": Colors.deepPurpleAccent,
  "indigoaccent": Colors.indigoAccent,
  "blueaccent": Colors.blueAccent,
  "lightblueaccent": Colors.lightBlueAccent,
  "cyanaccent": Colors.cyanAccent,
  "tealaccent": Colors.tealAccent,
  "greenaccent": Colors.greenAccent,
  "lightgreenaccent": Colors.lightGreenAccent,
  "limeaccent": Colors.limeAccent,
  "yellowaccent": Colors.yellowAccent,
  "amberaccent": Colors.amberAccent,
  "orangeaccent": Colors.orangeAccent,
  "deeporangeaccent": Colors.deepOrangeAccent,
};

// https://stackoverflow.com/questions/50081213/how-do-i-use-hexadecimal-color-strings-in-flutter
extension HexColor on Color {
  static Color? fromString(String colorString) {
    if (colorString.startsWith("#")) {
      return HexColor.fromHex(colorString);
    } else {
      return HexColor.fromNamedColor(colorString);
    }
  }

  static Color? fromNamedColor(String colorName) {
    RegExp namedColor = RegExp(r'^([a-zA-Z]+)([0-9]*)$');
    var matches = namedColor.allMatches(colorName);
    if (matches.isEmpty) {
      return null;
    }
    var name = matches.first.group(1);
    var shade = int.tryParse(matches.first.group(2)!) ?? 0;

    // find primary color
    MaterialColor? primaryColor = _materialColors[name!.toLowerCase()];
    if (primaryColor != null) {
      var shadedColor = primaryColor[shade];
      return shadedColor ?? primaryColor;
    }

    // accent color
    MaterialAccentColor? accentColor =
        _materialAccentColors[name.toLowerCase()];
    if (accentColor != null) {
      var shadedColor = accentColor[shade];
      return shadedColor ?? accentColor;
    }

    return null;
  }

  /// String is in the format "aabbcc" or "ffaabbcc" with an optional leading "#".
  static Color fromHex(String hexString) {
    final buffer = StringBuffer();
    if (hexString.length == 6 || hexString.length == 7) buffer.write('ff');
    buffer.write(hexString.replaceFirst('#', ''));
    return Color(int.parse(buffer.toString(), radix: 16));
  }

  /// Prefixes a hash sign if [leadingHashSign] is set to `true` (default is `true`).
  String toHex({bool leadingHashSign = true}) => '${leadingHashSign ? '#' : ''}'
      '${alpha.toRadixString(16).padLeft(2, '0')}'
      '${red.toRadixString(16).padLeft(2, '0')}'
      '${green.toRadixString(16).padLeft(2, '0')}'
      '${blue.toRadixString(16).padLeft(2, '0')}';
}
